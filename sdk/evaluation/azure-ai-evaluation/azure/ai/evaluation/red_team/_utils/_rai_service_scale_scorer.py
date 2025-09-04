# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import logging
from typing import List, Optional

from pyrit.models import Score, PromptRequestPiece, UnvalidatedScore
from pyrit.score.scorer import Scorer

from azure.ai.evaluation.simulator._model_tools._generated_rai_client import GeneratedRAIClient
from ._rai_service_eval_chat_target import RAIServiceEvalChatTarget
from .._attack_objective_generator import RiskCategory


class AzureRAIServiceScaleScorer(Scorer):
    """Scorer for Azure RAI service that returns a scale score.

    This class extends the PyRIT Scorer class to support scoring prompts using
    the Azure RAI service. It sends prompts to the RAI service and processes
    the responses to generate scores on a scale.

    This is a scale scorer that returns a float value between 0.0 and 1.0
    indicating how well a given prompt response achieves the specified objective.
    """

    scorer_type = "float_scale"

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
        evaluator_name: Optional[str] = None,
    ) -> None:
        """Initialize the scorer.

        :param client: The RAI client to use for scoring
        :param risk_category: The risk category for scoring
        :param credential: The credential for authentication
        :param azure_ai_project: The Azure AI project configuration
        :param api_version: Optional API version to use
        :param model: Optional model name to score with
        :param prompt_template_key: Optional prompt template key to use
        :param logger: Optional logger to use
        :param context: Optional context for scoring
        :param evaluator_name: Optional evaluator name identifier
        """
        super().__init__()
        self._client = client
        self._api_version = api_version
        self._model = model
        self._prompt_template_key = prompt_template_key
        self.logger = logger
        self.context = context
        self.evaluator_name = evaluator_name

        # Use RAIServiceEvalChatTarget for scoring
        self._scoring_target_red_llm = RAIServiceEvalChatTarget(
            logger=self.logger,
            credential=credential,
            azure_ai_project=azure_ai_project,
            risk_category=risk_category,
            context=context,
            evaluator_name=evaluator_name,
            scorer_type="float_scale",
        )

    async def score_async(
        self,
        request_response: PromptRequestPiece,
        *,
        task: Optional[str] = None,
    ) -> List[Score]:
        """Score a prompt response asynchronously.

        :param request_response: The prompt response to score (PromptRequestPiece)
        :param task: Optional task description (objective)
        :return: List of Score objects
        """
        self.logger.info(f"Starting to score prompt response with scale scorer")

        # Validate request_response
        self.validate(request_response, task=task)

        if not self._scoring_target_red_llm.context:
            self._scoring_target_red_llm.context = request_response.labels.get("context", "")

        unvalidated_score: UnvalidatedScore = await self._score_value_with_llm(
            prompt_target=self._scoring_target_red_llm,
            system_prompt="Please evaluate the following response on a scale.",
            prompt_request_value=request_response.converted_value,
            prompt_request_data_type=request_response.converted_value_data_type,
            scored_prompt_id=request_response.id,
            task=task,
            orchestrator_identifier=request_response.orchestrator_identifier,
        )

        # For scale scorer, we expect the raw_score_value to be a numeric score
        # The RAI service should return a score between 0 and the threshold
        # We need to normalize this to a 0.0-1.0 scale
        score = unvalidated_score.to_score(score_value=unvalidated_score.raw_score_value)

        return [score]

    def validate(self, request_response, *, task: Optional[str] = None):
        """Validates the request_response piece to score.

        This method checks if the request_response is valid for scoring by this scorer.

        :param request_response: The request response to be validated
        :param task: The task based on which the text should be scored (the original attacker model's objective)
        :raises: ValueError if the request_response is invalid
        """
        # Additional validation can be added here as needed
        pass
