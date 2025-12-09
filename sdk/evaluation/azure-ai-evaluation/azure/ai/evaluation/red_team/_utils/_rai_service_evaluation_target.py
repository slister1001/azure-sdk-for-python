# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import logging
import json
from typing import List, Optional

from azure.ai.evaluation.simulator._model_tools._generated_rai_client import GeneratedRAIClient
from azure.ai.evaluation._common.rai_service import evaluate_with_rai_service
from .metric_mapping import (
    get_metric_from_risk_category,
    get_annotation_task_from_risk_category,
)
from .._attack_objective_generator import RiskCategory
from pyrit.models import Message, construct_response_from_request
from pyrit.prompt_target import PromptChatTarget

logger = logging.getLogger(__name__)


class AzureRAIEvaluationTarget(PromptChatTarget):
    """Target for Azure RAI service evaluation (scoring)."""

    def __init__(
        self,
        *,
        client: GeneratedRAIClient,
        risk_category: RiskCategory,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        """Initialize the target.

        :param client: The RAI client
        :param risk_category: The risk category to evaluate
        :param logger: Optional logger
        """
        PromptChatTarget.__init__(self)
        self._client = client
        self.risk_category = risk_category
        self.logger = logger or logging.getLogger(__name__)

    async def send_prompt_async(self, *, message: Message) -> List[Message]:
        """Handle evaluation request using evaluate_with_rai_service."""
        self.logger.info("Starting send_prompt_async operation for evaluation")
        self._validate_request(message=message)

        request_piece = message.get_piece(0)
        # Extract the original value to evaluate (ignoring the prompt wrapper)
        thing_to_eval = request_piece.to_dict().get("original_value", request_piece.converted_value)
        
        thing_to_eval_qr = {"query": "query", "response": thing_to_eval, "context": ""}
        
        # If context is available in labels, use it
        if "context" in request_piece.labels:
            thing_to_eval_qr["context"] = request_piece.labels["context"]

        metric_name = get_metric_from_risk_category(self.risk_category)
        annotation_task = get_annotation_task_from_risk_category(self.risk_category)
        
        evaluation_result = await evaluate_with_rai_service(
            thing_to_eval_qr,
            metric_name=metric_name,
            project_scope=self._client.azure_ai_project,
            credential=self._client.token_manager, # GeneratedRAIClient stores credential in token_manager
            annotation_task=annotation_task,
        )
        self.logger.info(f"Evaluation result: {evaluation_result}")

        # Extract the relevant data from evaluation_result
        score = evaluation_result.get(f"{metric_name}_score", 0)
        reason = evaluation_result.get(f"{metric_name}_reason", "")
        threshold = evaluation_result.get(f"{metric_name}_threshold", 3)
        result = evaluation_result.get(metric_name, "")

        # Calculate pass/fail
        boolean_result = float(score) > float(threshold)

        # Format the response in a way that PyRIT's scorer can parse
        scorer_compatible_response = {
            "score_value": str(boolean_result).lower(),
            "description": f"Threshold: {threshold}, Result: {result}",
            "rationale": reason,
            "metadata": {
                "raw_score": score,
                "threshold": threshold,
                "result": result,
                "risk_category": self.risk_category,
            },
        }

        # Convert to JSON string
        response_json = json.dumps(scorer_compatible_response)

        # Construct the response
        response = construct_response_from_request(
            request=request_piece,
            response_text_pieces=[response_json],
        )
        return [response]

    def _validate_request(self, *, message: Message) -> None:
        """Validate the request.

        :param message: The prompt request message
        """
        if len(message.message_pieces) != 1:
            raise ValueError("This target only supports a single prompt request piece.")

        if message.get_piece(0).converted_value_data_type != "text":
            raise ValueError("This target only supports text prompt input.")

    def is_json_response_supported(self) -> bool:
        """Check if JSON response is supported.

        :return: True if JSON response is supported, False otherwise
        """
        return True
