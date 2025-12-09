# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import logging
from typing import List, Optional

from azure.ai.evaluation.simulator._model_tools._generated_rai_client import GeneratedRAIClient
from .._attack_objective_generator import RiskCategory
from pyrit.models import Message

from ._rai_service_simulation_target import AzureRAISimulationTarget, CrescendoResponse
from ._rai_service_evaluation_target import AzureRAIEvaluationTarget

logger = logging.getLogger(__name__)











class AzureRAIServiceTarget(AzureRAISimulationTarget):
    """Target for Azure RAI service.
    
    This class is a wrapper that supports both simulation (chat) and evaluation (scoring)
    for backward compatibility.
    """

    def __init__(
        self,
        *,
        client: GeneratedRAIClient,
        api_version: Optional[str] = None,
        model: Optional[str] = None,
        objective: Optional[str] = None,
        tense: Optional[str] = None,
        prompt_template_key: Optional[str] = None,
        logger: Optional[logging.Logger] = None,
        crescendo_format: bool = False,
        is_one_dp_project: bool = False,
        risk_category: Optional[RiskCategory] = None,
    ) -> None:
        """Initialize the target.

        :param client: The RAI client
        :param api_version: The API version to use
        :param model: The model to use
        :param objective: The objective of the target
        """
        super().__init__(
            client=client,
            api_version=api_version,
            model=model,
            objective=objective,
            tense=tense,
            prompt_template_key=prompt_template_key,
            logger=logger,
            crescendo_format=crescendo_format,
            is_one_dp_project=is_one_dp_project,
        )
        self.risk_category = risk_category
        self._evaluation_target = None
        if risk_category:
            self._evaluation_target = AzureRAIEvaluationTarget(
                client=client,
                risk_category=risk_category,
                logger=logger,
            )

    async def send_prompt_async(
        self, *, message: Message, objective: str = ""
    ) -> List[Message]:
        """Send a prompt to the Azure RAI service.

        :param message: The prompt request message
        :param objective: Optional objective to use for this specific request
        :return: The response
        """
        if self.risk_category and self._evaluation_target:
            return await self._evaluation_target.send_prompt_async(message=message)
        
        return await super().send_prompt_async(message=message, objective=objective)
