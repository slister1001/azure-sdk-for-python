# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import logging
import json
from typing import List, Optional

from pyrit.models import MessagePiece, Score, UnvalidatedScore
from pyrit.score.true_false.true_false_scorer import TrueFalseScorer
from pyrit.score.scorer_prompt_validator import ScorerPromptValidator

from azure.ai.evaluation.simulator._model_tools._generated_rai_client import GeneratedRAIClient
from ._rai_service_evaluation_target import AzureRAIEvaluationTarget
from .._attack_objective_generator import RiskCategory


class AzureRAIServiceTrueFalseScorer(TrueFalseScorer):
    """Scorer for Azure RAI service.

    This class extends the PyRIT Scorer class to support scoring prompts using
    the Azure RAI service. It sends prompts to the RAI service and processes
    the responses to generate scores.

    This is a true/false scorer that determines whether a given prompt response
    achieves the specified objective.
    """

    scorer_type = "true_false"

    def __init__(
        self,
        *,
        client: GeneratedRAIClient,
        risk_category: RiskCategory,
        credential,
        azure_ai_project,
        api_version: Optional[str] = None,
        model: Optional[str] = None,
        prompt_template_key: Optional[str] = None,
        logger: Optional[logging.Logger] = None,
        context: Optional[str] = None,
        validator: Optional[ScorerPromptValidator] = None,
    ) -> None:
        """Initialize the scorer.

        :param client: The RAI client to use for scoring
        :param api_version: Optional API version to use
        :param model: Optional model name to score with
        :param prompt_template_key: Optional prompt template key to use
        :param logger: Optional logger to use
        """
        self.logger = logger or logging.getLogger(__name__)
        self.context = context

        # Use AzureRAIEvaluationTarget for scoring
        self._scoring_target = AzureRAIEvaluationTarget(
            client=client,
            risk_category=risk_category,
            logger=self.logger,
        )
        
        validator = validator or ScorerPromptValidator(
            supported_data_types=("text",),
            supported_roles=("assistant",),
            max_pieces_in_response=1,
        )
        
        super().__init__(validator=validator)

    async def _score_piece_async(
        self, message_piece: MessagePiece, *, objective: Optional[str] = None
    ) -> List[Score]:
        """Score a single message piece using the Azure RAI service."""
        self.logger.info("Starting to score prompt response")
        
        value_to_score = message_piece.converted_value
        
        # Check if value is CrescendoResponse JSON and extract generated_question
        try:
            if isinstance(value_to_score, str) and "generated_question" in value_to_score:
                parsed = json.loads(value_to_score)
                if "generated_question" in parsed:
                    value_to_score = parsed["generated_question"]
                    self.logger.info(f"Extracted generated_question from CrescendoResponse for scoring: {value_to_score}")
        except Exception as e:
            self.logger.warning(f"Failed to parse potential CrescendoResponse: {e}")

        # Ensure context is available in message piece labels if not already
        if self.context and "context" not in message_piece.labels:
            message_piece.labels["context"] = self.context

        derived_objective = objective or message_piece.labels.get("objective")

        unvalidated_score: UnvalidatedScore = await self._score_value_with_llm(
            prompt_target=self._scoring_target,
            system_prompt="Please evaluate the following response.",
            message_value=value_to_score,
            message_data_type=message_piece.converted_value_data_type,
            scored_prompt_id=str(message_piece.id),
            objective=derived_objective,
            attack_identifier=message_piece.attack_identifier or None,
        )
        score = unvalidated_score.to_score(
            score_value=unvalidated_score.raw_score_value,
            score_type=self.scorer_type,
        )

        return [score]


