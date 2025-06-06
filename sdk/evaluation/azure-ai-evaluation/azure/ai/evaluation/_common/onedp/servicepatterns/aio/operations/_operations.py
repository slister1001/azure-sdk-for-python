# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) Python Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
from azure.core import AsyncPipelineClient

from ...._serialization import Deserializer, Serializer
from ....aio._configuration import AIProjectClientConfiguration
from ...buildingblocks.aio.operations._operations import ServicePatternsBuildingBlocksOperations


class ServicePatternsOperations:
    """
    .. warning::
        **DO NOT** instantiate this class directly.

        Instead, you should access the following operations through
        :class:`~azure.ai.projects.aio.AIProjectClient`'s
        :attr:`service_patterns` attribute.
    """

    def __init__(self, *args, **kwargs) -> None:
        input_args = list(args)
        self._client: AsyncPipelineClient = input_args.pop(0) if input_args else kwargs.pop("client")
        self._config: AIProjectClientConfiguration = input_args.pop(0) if input_args else kwargs.pop("config")
        self._serialize: Serializer = input_args.pop(0) if input_args else kwargs.pop("serializer")
        self._deserialize: Deserializer = input_args.pop(0) if input_args else kwargs.pop("deserializer")

        self.building_blocks = ServicePatternsBuildingBlocksOperations(
            self._client, self._config, self._serialize, self._deserialize
        )
