# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import logging
from typing import List, Optional

from azure.ai.evaluation.simulator._model_tools._generated_rai_client import GeneratedRAIClient
from .._attack_objective_generator import RiskCategory
from pyrit.models import Message

from ._rai_service_evaluation_target import AzureRAIEvaluationTarget
from pyrit.prompt_target import PromptChatTarget

logger = logging.getLogger(__name__)


class AzureRAIServiceTarget(PromptChatTarget):
    """Base target for Azure RAI service.
    
    This class provides the base functionality for Azure RAI service targets.
    """

    def __init__(
        self,
        *,
        client: GeneratedRAIClient,
        api_version: Optional[str] = None,
        model: Optional[str] = None,
        objective: Optional[str] = None,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        """Initialize the target.

        :param client: The RAI client
        :param api_version: The API version to use
        :param model: The model to use
        :param objective: The objective of the target
        :param logger: The logger to use
        """
        PromptChatTarget.__init__(self)
        self._client = client
        self._api_version = api_version
        self._model = model
        self.objective = objective
        self.logger = logger or logging.getLogger(__name__)

    async def send_prompt_async(
        self, *, message: Message, objective: str = ""
    ) -> List[Message]:
        """Send a prompt to the Azure RAI service.

        :param message: The prompt request message
        :param objective: Optional objective to use for this specific request
        :return: The response
        """
        raise NotImplementedError("Subclasses must implement send_prompt_async")

    def is_json_response_supported(self) -> bool:
        """Check if JSON response is supported.

        :return: True if JSON response is supported, False otherwise
        """
        return True
