# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Utilities for executing prompt-sending attack routines."""

import asyncio
import logging
import os
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import tenacity

from pyrit.executor.attack import AttackConverterConfig, AttackScoringConfig
from pyrit.executor.attack.single_turn.prompt_sending import PromptSendingAttack
from pyrit.prompt_converter import PromptConverter
from pyrit.prompt_normalizer import PromptConverterConfiguration
from pyrit.prompt_target import PromptChatTarget

from ._attack_objective_generator import RiskCategory
from ._attack_strategy import AttackStrategy
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


def _flatten_prompt_converters(converter: Union[PromptConverter, List[PromptConverter], None]) -> List[PromptConverter]:
    """Normalize converter definitions into a flat list of PromptConverter instances."""

    if converter is None:
        return []

    if isinstance(converter, PromptConverter):
        return [converter]

    flattened: List[PromptConverter] = []
    if isinstance(converter, (list, tuple)):
        for item in converter:
            flattened.extend(_flatten_prompt_converters(item))

    return [conv for conv in flattened if isinstance(conv, PromptConverter)]


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
    converter: Union[PromptConverter, List[PromptConverter], None],
    timeout: int,
    data_file_path: str,
    logger: logging.Logger,
    retry_manager: Optional[RetryManager],
    prompt_to_context: Optional[Dict[str, Any]],
    prompt_to_risk_subtype: Optional[Dict[str, Any]],
    task_statuses: Dict[str, str],
    red_team_info: Dict[str, Dict[str, Dict[str, Any]]],
    chat_target: PromptChatTarget,
) -> None:
    """Execute a single-turn attack flow using PyRIT's PromptSendingAttack primitives."""

    if not prompts:
        logger.warning(
            "No prompts provided to PromptSendingAttack for %s/%s; skipping execution.",
            strategy_name,
            risk_category.value,
        )
        return

    converters = _flatten_prompt_converters(converter)
    request_configurations = PromptConverterConfiguration.from_converters(converters=converters)
    attack_converter_config = AttackConverterConfig(request_converters=request_configurations)
    attack = PromptSendingAttack(
        objective_target=chat_target,
        attack_converter_config=attack_converter_config,
        attack_scoring_config=AttackScoringConfig(),
    )

    calculated_timeout = calculate_prompt_timeout(timeout, strategy)

    for prompt_idx, prompt in enumerate(prompts):
        prompt_start_time = datetime.now()
        context_dict = _normalize_context_for_prompt(prompt, prompt_to_context)
        risk_sub_type = prompt_to_risk_subtype.get(prompt) if prompt_to_risk_subtype else None

        memory_labels: Dict[str, Any] = {
            "risk_strategy_path": data_file_path,
            "batch": prompt_idx + 1,
            "context": context_dict,
        }
        if risk_sub_type:
            memory_labels["risk_sub_type"] = risk_sub_type

        async def _execute_attack() -> None:
            await asyncio.wait_for(
                attack.execute_async(objective=prompt, memory_labels=memory_labels),
                timeout=calculated_timeout,
            )

        retry_decorator = None
        if retry_manager is not None:
            retry_decorator = retry_manager.create_retry_decorator(
                context=f"prompt_sending:{strategy_name}:{risk_category.value}:prompt_{prompt_idx + 1}"
            )

        execute_with_retry = retry_decorator(_execute_attack) if retry_decorator else _execute_attack

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
                "Error processing prompt %d for %s/%s: %s",
                prompt_idx + 1,
                strategy_name,
                risk_category.value,
                str(exc),
            )
            red_team_info[strategy_name][risk_category.value]["status"] = TASK_STATUS["INCOMPLETE"]
            continue


__all__ = [
    "ensure_data_file_path",
    "calculate_prompt_timeout",
    "run_prompt_sending_attack_flow",
]
