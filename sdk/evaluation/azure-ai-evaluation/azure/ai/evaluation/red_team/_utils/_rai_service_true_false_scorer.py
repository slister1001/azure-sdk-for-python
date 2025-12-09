# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import logging
from typing import List, Optional

from pyrit.models import MessagePiece, Score, UnvalidatedScore
from pyrit.score.scorer import Scorer
from pyrit.score.scorer_prompt_validator import ScorerPromptValidator

from azure.ai.evaluation.simulator._model_tools._generated_rai_client import GeneratedRAIClient
from ._rai_service_eval_chat_target import RAIServiceEvalChatTarget
from .._attack_objective_generator import RiskCategory


class AzureRAIServiceTrueFalseScorer(Scorer):
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
        validator = validator or ScorerPromptValidator(
            supported_data_types=("text",),
            supported_roles=("assistant",),
            max_pieces_in_response=1,
        )
        super().__init__(validator=validator)
        self._client = client
        self._api_version = api_version
        self._model = model
        self._prompt_template_key = prompt_template_key
        self.logger = logger or logging.getLogger(__name__)
        self.context = context

        # Use AzureRAIServiceTarget for scoring as well
        self._scoring_target_red_llm = RAIServiceEvalChatTarget(
            logger=self.logger,
            credential=credential,
            azure_ai_project=azure_ai_project,
            risk_category=risk_category,
            context=context,
        )

    async def _score_piece_async(
        self, message_piece: MessagePiece, *, objective: Optional[str] = None
    ) -> List[Score]:
        """Score a single message piece using the Azure RAI service."""
        self.logger.info("Starting to score prompt response")

        if not self._scoring_target_red_llm.context:
            self._scoring_target_red_llm.context = message_piece.labels.get("context", "")

        derived_objective = objective or message_piece.labels.get("objective")

        unvalidated_score: UnvalidatedScore = await self._score_value_with_llm(
            prompt_target=self._scoring_target_red_llm,
            system_prompt="Please evaluate the following response.",
            message_value=message_piece.converted_value,
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

    def validate_return_scores(self, scores: List[Score]):
        """Ensure returned scores align with the expected scorer type."""
        for score in scores:
            if score.score_type != self.scorer_type:
                raise ValueError(
                    f"Score type {score.score_type} does not match expected {self.scorer_type} for {self.__class__.__name__}."
                )
