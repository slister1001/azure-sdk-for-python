# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Utilities for executing prompt-sending attack routines."""

import asyncio
import logging
import os
import uuid
import traceback
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import tenacity
from pyrit.score import TrueFalseScorer

from azure.ai.evaluation.simulator._model_tools._generated_rai_client import GeneratedRAIClient
from pyrit.executor.attack import AttackScoringConfig
from pyrit.scenario import FoundryScenario
from pyrit.scenario.scenarios.foundry_scenario import FoundryStrategy
from pyrit.prompt_target import PromptChatTarget

from ._attack_objective_generator import RiskCategory
from ._attack_strategy import AttackStrategy
from ._strategy_mapping import map_to_foundry_strategy, requires_custom_handling
from ._utils._rai_service_true_false_scorer import AzureRAIServiceTrueFalseScorer
from ._utils._rai_service_target import AzureRAIServiceTarget
from ._utils.constants import DATA_EXT, TASK_STATUS
from ._utils.retry_utils import RetryManager


def ensure_data_file_path(
    red_team_info: Dict[str, Dict[str, Dict[str, Any]]],
    scan_output_dir: Optional[str],
    strategy_name: str,
    risk_category: RiskCategory,
) -> str:
    """Ensure the tracking entry has a data file path and return it."""

    strategy_entry = red_team_info.setdefault(strategy_name, {})
    category_entry = strategy_entry.setdefault(risk_category.value, {})

    current_path = category_entry.get("data_file")
    if current_path:
        return current_path

    file_name = f"{uuid.uuid4()}{DATA_EXT}"
    data_path = os.path.join(scan_output_dir, file_name) if scan_output_dir else file_name
    category_entry["data_file"] = data_path
    return data_path


def calculate_prompt_timeout(base_timeout: int, strategy: Union[AttackStrategy, List[AttackStrategy]]) -> int:
    """Scale the per-prompt timeout for strategies that tend to run longer."""

    if isinstance(strategy, AttackStrategy):
        strategies: List[AttackStrategy] = [strategy]
    elif isinstance(strategy, list):
        strategies = [item for item in strategy if isinstance(item, AttackStrategy)]
    else:
        strategies = []

    multiplier = 1.0
    if any(item is AttackStrategy.Crescendo for item in strategies):
        multiplier = 4.0
    elif any(item is AttackStrategy.MultiTurn for item in strategies):
        multiplier = 3.0

    return max(1, int(base_timeout * multiplier))


def _normalize_context_for_prompt(prompt: str, prompt_to_context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Normalize stored context data into the structure expected for memory labels."""

    context_data: Any = prompt_to_context.get(prompt, {}) if prompt_to_context else {}

    if isinstance(context_data, str):
        return {"contexts": [{"content": context_data}]} if context_data else {"contexts": []}

    if isinstance(context_data, dict):
        contexts = context_data.get("contexts")
        if isinstance(contexts, list):
            return {"contexts": contexts}

    return {"contexts": []}


async def run_prompt_sending_attack_flow(
    *,
    strategy_name: str,
    strategy: Union[AttackStrategy, List[AttackStrategy]],
    risk_category: RiskCategory,
    prompts: List[str],
    timeout: int,
    data_file_path: str,
    logger: logging.Logger,
    retry_manager: Optional[RetryManager],
    prompt_to_context: Optional[Dict[str, Any]],
    prompt_to_risk_subtype: Optional[Dict[str, Any]],
    task_statuses: Dict[str, str],
    red_team_info: Dict[str, Dict[str, Dict[str, Any]]],
    rai_client: GeneratedRAIClient,
    credential: Any,
    azure_ai_project: Any,
    chat_target: PromptChatTarget,
    is_one_dp_project: bool,
) -> None:
    """Execute attacks using PyRIT's FoundryScenario with one AtomicAttack per prompt.

    This function leverages FoundryScenario's orchestration capabilities while maintaining
    per-prompt granularity for context and scoring. Each prompt is executed as a separate
    atomic attack with its own scorer instance and memory labels.

    :param strategy_name: Display name for the strategy being executed
    :param strategy: AttackStrategy or list of strategies to use
    :param risk_category: Risk category for this attack run
    :param prompts: List of objective prompts to execute
    :param timeout: Base timeout in seconds per prompt
    :param data_file_path: Path to the data file for tracking
    :param logger: Logger instance for diagnostic output
    :param retry_manager: Optional retry configuration for transient failures
    :param prompt_to_context: Mapping from prompt to context metadata
    :param prompt_to_risk_subtype: Mapping from prompt to risk subtype
    :param task_statuses: Dict tracking status of each task
    :param red_team_info: Dict tracking overall red team execution state
    :param rai_client: Authenticated RAI client for scoring
    :param credential: Credential to authorize scoring requests
    :param azure_ai_project: Azure AI project scope metadata
    :param chat_target: PyRIT target for objective execution
    :param is_one_dp_project: Whether this is a OneDP project
    """

    if not prompts:
        logger.warning(
            "No prompts provided to FoundryScenario for %s/%s; skipping execution.",
            strategy_name,
            risk_category.value,
        )
        return

    # Map AttackStrategy to FoundryStrategy
    strategies = [strategy] if isinstance(strategy, AttackStrategy) else strategy
    mapped_strategies = []
    
    for strat in strategies:
        if requires_custom_handling(strat):
            logger.warning(
                "Strategy %s requires custom handling; falling back to baseline execution.",
                strat.value,
            )
            # For IndirectJailbreak/Baseline, use Jailbreak as closest equivalent
            mapped_strategies.append(FoundryStrategy.Jailbreak)
        else:
            foundry_strat = map_to_foundry_strategy(strat)
            if foundry_strat:
                mapped_strategies.append(foundry_strat)

    if not mapped_strategies:
        logger.error("No valid FoundryStrategy mapping found for %s", strategy_name)
        return

    calculated_timeout = calculate_prompt_timeout(timeout, strategy)

    # Execute each prompt as a separate atomic attack to preserve per-prompt context
    for prompt_idx, prompt in enumerate(prompts):
        prompt_start_time = datetime.now()
        context_dict = _normalize_context_for_prompt(prompt, prompt_to_context)
        risk_sub_type = prompt_to_risk_subtype.get(prompt) if prompt_to_risk_subtype else None

        contexts = context_dict.get("contexts", [])
        context_string = ""
        if contexts:
            context_string = "\n".join(
                ctx.get("content", "") if isinstance(ctx, dict) else str(ctx) for ctx in contexts
            )

        # Create a scorer tailored to this prompt so context stays accurate
        objective_scorer = AzureRAIServiceTrueFalseScorer(
            client=rai_client,
            risk_category=risk_category,
            credential=credential,
            azure_ai_project=azure_ai_project,
            logger=logger,
            context=context_string,
        )

        # Build memory labels for this specific prompt
        memory_labels: Dict[str, Any] = {
            "risk_strategy_path": data_file_path,
            "batch": prompt_idx + 1,
            "context": context_dict,
            "strategy_name": strategy_name,
        }
        if risk_sub_type:
            memory_labels["risk_sub_type"] = risk_sub_type

        # Configure adversarial chat (attacker)
        prompt_template_key = "orchestrators/red_teaming/text_generation.yaml"
        crescendo_format = False

        if any(s == AttackStrategy.Crescendo for s in strategies):
            prompt_template_key = "orchestrators/crescendo/crescendo_variant_1.yaml"
            crescendo_format = True

        adversarial_chat = AzureRAIServiceTarget(
            client=rai_client,
            api_version=None,
            model="gpt-4",
            prompt_template_key=prompt_template_key,
            objective=prompt,
            logger=logger,
            crescendo_format=crescendo_format,
            is_one_dp_project=is_one_dp_project,
        )

        # Create a scenario with a single objective for this prompt
        scenario = FoundryScenario(
            adversarial_chat=adversarial_chat,
            objectives=[prompt],
            objective_scorer=objective_scorer,
            include_baseline=False
        )

        async def _execute_scenario() -> None:
            """Execute the scenario with timeout and proper initialization."""
            await scenario.initialize_async(
                objective_target=chat_target,
                scenario_strategies=mapped_strategies,
                memory_labels=memory_labels,
            )
            
            await asyncio.wait_for(
                scenario.run_async(),
                timeout=calculated_timeout,
            )

        retry_decorator = None
        if retry_manager is not None:
            retry_decorator = retry_manager.create_retry_decorator(
                context=f"foundry_scenario:{strategy_name}:{risk_category.value}:prompt_{prompt_idx + 1}"
            )

        execute_with_retry = retry_decorator(_execute_scenario) if retry_decorator else _execute_scenario

        try:
            await execute_with_retry()
            prompt_duration = (datetime.now() - prompt_start_time).total_seconds()
            logger.debug(
                "Successfully processed prompt %d/%d for %s/%s in %.2f seconds",
                prompt_idx + 1,
                len(prompts),
                strategy_name,
                risk_category.value,
                prompt_duration,
            )

            if prompt_idx < len(prompts) - 1:
                print(
                    f"Strategy {strategy_name}, Risk {risk_category.value}: Processed prompt {prompt_idx+1}/{len(prompts)}"
                )

        except (asyncio.TimeoutError, tenacity.RetryError):
            logger.warning(
                "Prompt %d for %s/%s timed out after %s seconds; continuing with remaining prompts.",
                prompt_idx + 1,
                strategy_name,
                risk_category.value,
                calculated_timeout,
            )
            print(f"⚠️ TIMEOUT: Strategy {strategy_name}, Risk {risk_category.value}, Prompt {prompt_idx+1}")
            task_key = f"{strategy_name}_{risk_category.value}_prompt_{prompt_idx+1}"
            task_statuses[task_key] = TASK_STATUS["TIMEOUT"]
            red_team_info[strategy_name][risk_category.value]["status"] = TASK_STATUS["INCOMPLETE"]
            continue
        except Exception as exc:  # pylint: disable=broad-except
            logger.error(
                "Error processing prompt %d for %s/%s: %s\n%s",
                prompt_idx + 1,
                strategy_name,
                risk_category.value,
                str(exc),
                traceback.format_exc(),
            )
            red_team_info[strategy_name][risk_category.value]["status"] = TASK_STATUS["INCOMPLETE"]
            continue


__all__ = [
    "ensure_data_file_path",
    "calculate_prompt_timeout",
    "run_prompt_sending_attack_flow",
]
