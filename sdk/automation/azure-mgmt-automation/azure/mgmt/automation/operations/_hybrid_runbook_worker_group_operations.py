# pylint: disable=too-many-lines,too-many-statements
# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
from io import IOBase
import sys
from typing import Any, Callable, Dict, IO, Iterable, Optional, Type, TypeVar, Union, overload

from azure.core.exceptions import (
    ClientAuthenticationError,
    HttpResponseError,
    ResourceExistsError,
    ResourceNotFoundError,
    ResourceNotModifiedError,
    map_error,
)
from azure.core.paging import ItemPaged
from azure.core.pipeline import PipelineResponse
from azure.core.rest import HttpRequest, HttpResponse
from azure.core.tracing.decorator import distributed_trace
from azure.core.utils import case_insensitive_dict
from azure.mgmt.core.exceptions import ARMErrorFormat

from .. import models as _models
from .._serialization import Serializer

if sys.version_info >= (3, 9):
    from collections.abc import MutableMapping
else:
    from typing import MutableMapping  # type: ignore  # pylint: disable=ungrouped-imports
T = TypeVar("T")
ClsType = Optional[Callable[[PipelineResponse[HttpRequest, HttpResponse], T, Dict[str, Any]], Any]]

_SERIALIZER = Serializer()
_SERIALIZER.client_side_validation = False


def build_delete_request(
    resource_group_name: str,
    automation_account_name: str,
    hybrid_runbook_worker_group_name: str,
    subscription_id: str,
    **kwargs: Any
) -> HttpRequest:
    _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
    _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

    api_version: str = kwargs.pop("api_version", _params.pop("api-version", "2022-08-08"))
    accept = _headers.pop("Accept", "application/json")

    # Construct URL
    _url = kwargs.pop(
        "template_url",
        "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Automation/automationAccounts/{automationAccountName}/hybridRunbookWorkerGroups/{hybridRunbookWorkerGroupName}",
    )  # pylint: disable=line-too-long
    path_format_arguments = {
        "resourceGroupName": _SERIALIZER.url(
            "resource_group_name", resource_group_name, "str", max_length=90, min_length=1, pattern=r"^[-\w\._]+$"
        ),
        "automationAccountName": _SERIALIZER.url("automation_account_name", automation_account_name, "str"),
        "hybridRunbookWorkerGroupName": _SERIALIZER.url(
            "hybrid_runbook_worker_group_name", hybrid_runbook_worker_group_name, "str"
        ),
        "subscriptionId": _SERIALIZER.url("subscription_id", subscription_id, "str"),
    }

    _url: str = _url.format(**path_format_arguments)  # type: ignore

    # Construct parameters
    _params["api-version"] = _SERIALIZER.query("api_version", api_version, "str")

    # Construct headers
    _headers["Accept"] = _SERIALIZER.header("accept", accept, "str")

    return HttpRequest(method="DELETE", url=_url, params=_params, headers=_headers, **kwargs)


def build_get_request(
    resource_group_name: str,
    automation_account_name: str,
    hybrid_runbook_worker_group_name: str,
    subscription_id: str,
    **kwargs: Any
) -> HttpRequest:
    _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
    _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

    api_version: str = kwargs.pop("api_version", _params.pop("api-version", "2022-08-08"))
    accept = _headers.pop("Accept", "application/json")

    # Construct URL
    _url = kwargs.pop(
        "template_url",
        "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Automation/automationAccounts/{automationAccountName}/hybridRunbookWorkerGroups/{hybridRunbookWorkerGroupName}",
    )  # pylint: disable=line-too-long
    path_format_arguments = {
        "resourceGroupName": _SERIALIZER.url(
            "resource_group_name", resource_group_name, "str", max_length=90, min_length=1, pattern=r"^[-\w\._]+$"
        ),
        "automationAccountName": _SERIALIZER.url("automation_account_name", automation_account_name, "str"),
        "hybridRunbookWorkerGroupName": _SERIALIZER.url(
            "hybrid_runbook_worker_group_name", hybrid_runbook_worker_group_name, "str"
        ),
        "subscriptionId": _SERIALIZER.url("subscription_id", subscription_id, "str"),
    }

    _url: str = _url.format(**path_format_arguments)  # type: ignore

    # Construct parameters
    _params["api-version"] = _SERIALIZER.query("api_version", api_version, "str")

    # Construct headers
    _headers["Accept"] = _SERIALIZER.header("accept", accept, "str")

    return HttpRequest(method="GET", url=_url, params=_params, headers=_headers, **kwargs)


def build_create_request(
    resource_group_name: str,
    automation_account_name: str,
    hybrid_runbook_worker_group_name: str,
    subscription_id: str,
    **kwargs: Any
) -> HttpRequest:
    _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
    _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

    api_version: str = kwargs.pop("api_version", _params.pop("api-version", "2022-08-08"))
    content_type: Optional[str] = kwargs.pop("content_type", _headers.pop("Content-Type", None))
    accept = _headers.pop("Accept", "application/json")

    # Construct URL
    _url = kwargs.pop(
        "template_url",
        "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Automation/automationAccounts/{automationAccountName}/hybridRunbookWorkerGroups/{hybridRunbookWorkerGroupName}",
    )  # pylint: disable=line-too-long
    path_format_arguments = {
        "resourceGroupName": _SERIALIZER.url(
            "resource_group_name", resource_group_name, "str", max_length=90, min_length=1, pattern=r"^[-\w\._]+$"
        ),
        "automationAccountName": _SERIALIZER.url("automation_account_name", automation_account_name, "str"),
        "hybridRunbookWorkerGroupName": _SERIALIZER.url(
            "hybrid_runbook_worker_group_name", hybrid_runbook_worker_group_name, "str"
        ),
        "subscriptionId": _SERIALIZER.url("subscription_id", subscription_id, "str"),
    }

    _url: str = _url.format(**path_format_arguments)  # type: ignore

    # Construct parameters
    _params["api-version"] = _SERIALIZER.query("api_version", api_version, "str")

    # Construct headers
    if content_type is not None:
        _headers["Content-Type"] = _SERIALIZER.header("content_type", content_type, "str")
    _headers["Accept"] = _SERIALIZER.header("accept", accept, "str")

    return HttpRequest(method="PUT", url=_url, params=_params, headers=_headers, **kwargs)


def build_update_request(
    resource_group_name: str,
    automation_account_name: str,
    hybrid_runbook_worker_group_name: str,
    subscription_id: str,
    **kwargs: Any
) -> HttpRequest:
    _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
    _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

    api_version: str = kwargs.pop("api_version", _params.pop("api-version", "2022-08-08"))
    content_type: Optional[str] = kwargs.pop("content_type", _headers.pop("Content-Type", None))
    accept = _headers.pop("Accept", "application/json")

    # Construct URL
    _url = kwargs.pop(
        "template_url",
        "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Automation/automationAccounts/{automationAccountName}/hybridRunbookWorkerGroups/{hybridRunbookWorkerGroupName}",
    )  # pylint: disable=line-too-long
    path_format_arguments = {
        "resourceGroupName": _SERIALIZER.url(
            "resource_group_name", resource_group_name, "str", max_length=90, min_length=1, pattern=r"^[-\w\._]+$"
        ),
        "automationAccountName": _SERIALIZER.url("automation_account_name", automation_account_name, "str"),
        "hybridRunbookWorkerGroupName": _SERIALIZER.url(
            "hybrid_runbook_worker_group_name", hybrid_runbook_worker_group_name, "str"
        ),
        "subscriptionId": _SERIALIZER.url("subscription_id", subscription_id, "str"),
    }

    _url: str = _url.format(**path_format_arguments)  # type: ignore

    # Construct parameters
    _params["api-version"] = _SERIALIZER.query("api_version", api_version, "str")

    # Construct headers
    if content_type is not None:
        _headers["Content-Type"] = _SERIALIZER.header("content_type", content_type, "str")
    _headers["Accept"] = _SERIALIZER.header("accept", accept, "str")

    return HttpRequest(method="PATCH", url=_url, params=_params, headers=_headers, **kwargs)


def build_list_by_automation_account_request(
    resource_group_name: str,
    automation_account_name: str,
    subscription_id: str,
    *,
    filter: Optional[str] = None,
    **kwargs: Any
) -> HttpRequest:
    _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
    _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

    api_version: str = kwargs.pop("api_version", _params.pop("api-version", "2022-08-08"))
    accept = _headers.pop("Accept", "application/json")

    # Construct URL
    _url = kwargs.pop(
        "template_url",
        "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Automation/automationAccounts/{automationAccountName}/hybridRunbookWorkerGroups",
    )  # pylint: disable=line-too-long
    path_format_arguments = {
        "resourceGroupName": _SERIALIZER.url(
            "resource_group_name", resource_group_name, "str", max_length=90, min_length=1, pattern=r"^[-\w\._]+$"
        ),
        "automationAccountName": _SERIALIZER.url("automation_account_name", automation_account_name, "str"),
        "subscriptionId": _SERIALIZER.url("subscription_id", subscription_id, "str"),
    }

    _url: str = _url.format(**path_format_arguments)  # type: ignore

    # Construct parameters
    if filter is not None:
        _params["$filter"] = _SERIALIZER.query("filter", filter, "str")
    _params["api-version"] = _SERIALIZER.query("api_version", api_version, "str")

    # Construct headers
    _headers["Accept"] = _SERIALIZER.header("accept", accept, "str")

    return HttpRequest(method="GET", url=_url, params=_params, headers=_headers, **kwargs)


class HybridRunbookWorkerGroupOperations:
    """
    .. warning::
        **DO NOT** instantiate this class directly.

        Instead, you should access the following operations through
        :class:`~azure.mgmt.automation.AutomationClient`'s
        :attr:`hybrid_runbook_worker_group` attribute.
    """

    models = _models

    def __init__(self, *args, **kwargs):
        input_args = list(args)
        self._client = input_args.pop(0) if input_args else kwargs.pop("client")
        self._config = input_args.pop(0) if input_args else kwargs.pop("config")
        self._serialize = input_args.pop(0) if input_args else kwargs.pop("serializer")
        self._deserialize = input_args.pop(0) if input_args else kwargs.pop("deserializer")

    @distributed_trace
    def delete(  # pylint: disable=inconsistent-return-statements
        self,
        resource_group_name: str,
        automation_account_name: str,
        hybrid_runbook_worker_group_name: str,
        **kwargs: Any
    ) -> None:
        """Delete a hybrid runbook worker group.

        .. seealso::
           - http://aka.ms/azureautomationsdk/hybridrunbookworkergroupoperations

        :param resource_group_name: Name of an Azure Resource group. Required.
        :type resource_group_name: str
        :param automation_account_name: The name of the automation account. Required.
        :type automation_account_name: str
        :param hybrid_runbook_worker_group_name: The hybrid runbook worker group name. Required.
        :type hybrid_runbook_worker_group_name: str
        :return: None or the result of cls(response)
        :rtype: None
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map: MutableMapping[int, Type[HttpResponseError]] = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: str = kwargs.pop("api_version", _params.pop("api-version", "2022-08-08"))
        cls: ClsType[None] = kwargs.pop("cls", None)

        _request = build_delete_request(
            resource_group_name=resource_group_name,
            automation_account_name=automation_account_name,
            hybrid_runbook_worker_group_name=hybrid_runbook_worker_group_name,
            subscription_id=self._config.subscription_id,
            api_version=api_version,
            headers=_headers,
            params=_params,
        )
        _request.url = self._client.format_url(_request.url)

        _stream = False
        pipeline_response: PipelineResponse = self._client._pipeline.run(  # pylint: disable=protected-access
            _request, stream=_stream, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.ErrorResponse, pipeline_response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        if cls:
            return cls(pipeline_response, None, {})  # type: ignore

    @distributed_trace
    def get(
        self,
        resource_group_name: str,
        automation_account_name: str,
        hybrid_runbook_worker_group_name: str,
        **kwargs: Any
    ) -> _models.HybridRunbookWorkerGroup:
        """Retrieve a hybrid runbook worker group.

        .. seealso::
           - http://aka.ms/azureautomationsdk/hybridrunbookworkergroupoperations

        :param resource_group_name: Name of an Azure Resource group. Required.
        :type resource_group_name: str
        :param automation_account_name: The name of the automation account. Required.
        :type automation_account_name: str
        :param hybrid_runbook_worker_group_name: The hybrid runbook worker group name. Required.
        :type hybrid_runbook_worker_group_name: str
        :return: HybridRunbookWorkerGroup or the result of cls(response)
        :rtype: ~azure.mgmt.automation.models.HybridRunbookWorkerGroup
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map: MutableMapping[int, Type[HttpResponseError]] = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: str = kwargs.pop("api_version", _params.pop("api-version", "2022-08-08"))
        cls: ClsType[_models.HybridRunbookWorkerGroup] = kwargs.pop("cls", None)

        _request = build_get_request(
            resource_group_name=resource_group_name,
            automation_account_name=automation_account_name,
            hybrid_runbook_worker_group_name=hybrid_runbook_worker_group_name,
            subscription_id=self._config.subscription_id,
            api_version=api_version,
            headers=_headers,
            params=_params,
        )
        _request.url = self._client.format_url(_request.url)

        _stream = False
        pipeline_response: PipelineResponse = self._client._pipeline.run(  # pylint: disable=protected-access
            _request, stream=_stream, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.ErrorResponse, pipeline_response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        deserialized = self._deserialize("HybridRunbookWorkerGroup", pipeline_response.http_response)

        if cls:
            return cls(pipeline_response, deserialized, {})  # type: ignore

        return deserialized  # type: ignore

    @overload
    def create(
        self,
        resource_group_name: str,
        automation_account_name: str,
        hybrid_runbook_worker_group_name: str,
        hybrid_runbook_worker_group_creation_parameters: _models.HybridRunbookWorkerGroupCreateOrUpdateParameters,
        *,
        content_type: str = "application/json",
        **kwargs: Any
    ) -> _models.HybridRunbookWorkerGroup:
        """Create a hybrid runbook worker group.

        .. seealso::
           - http://aka.ms/azureautomationsdk/hybridrunbookworkergroupoperations

        :param resource_group_name: Name of an Azure Resource group. Required.
        :type resource_group_name: str
        :param automation_account_name: The name of the automation account. Required.
        :type automation_account_name: str
        :param hybrid_runbook_worker_group_name: The hybrid runbook worker group name. Required.
        :type hybrid_runbook_worker_group_name: str
        :param hybrid_runbook_worker_group_creation_parameters: The create or update parameters for
         hybrid runbook worker group. Required.
        :type hybrid_runbook_worker_group_creation_parameters:
         ~azure.mgmt.automation.models.HybridRunbookWorkerGroupCreateOrUpdateParameters
        :keyword content_type: Body Parameter content-type. Content type parameter for JSON body.
         Default value is "application/json".
        :paramtype content_type: str
        :return: HybridRunbookWorkerGroup or the result of cls(response)
        :rtype: ~azure.mgmt.automation.models.HybridRunbookWorkerGroup
        :raises ~azure.core.exceptions.HttpResponseError:
        """

    @overload
    def create(
        self,
        resource_group_name: str,
        automation_account_name: str,
        hybrid_runbook_worker_group_name: str,
        hybrid_runbook_worker_group_creation_parameters: IO[bytes],
        *,
        content_type: str = "application/json",
        **kwargs: Any
    ) -> _models.HybridRunbookWorkerGroup:
        """Create a hybrid runbook worker group.

        .. seealso::
           - http://aka.ms/azureautomationsdk/hybridrunbookworkergroupoperations

        :param resource_group_name: Name of an Azure Resource group. Required.
        :type resource_group_name: str
        :param automation_account_name: The name of the automation account. Required.
        :type automation_account_name: str
        :param hybrid_runbook_worker_group_name: The hybrid runbook worker group name. Required.
        :type hybrid_runbook_worker_group_name: str
        :param hybrid_runbook_worker_group_creation_parameters: The create or update parameters for
         hybrid runbook worker group. Required.
        :type hybrid_runbook_worker_group_creation_parameters: IO[bytes]
        :keyword content_type: Body Parameter content-type. Content type parameter for binary body.
         Default value is "application/json".
        :paramtype content_type: str
        :return: HybridRunbookWorkerGroup or the result of cls(response)
        :rtype: ~azure.mgmt.automation.models.HybridRunbookWorkerGroup
        :raises ~azure.core.exceptions.HttpResponseError:
        """

    @distributed_trace
    def create(
        self,
        resource_group_name: str,
        automation_account_name: str,
        hybrid_runbook_worker_group_name: str,
        hybrid_runbook_worker_group_creation_parameters: Union[
            _models.HybridRunbookWorkerGroupCreateOrUpdateParameters, IO[bytes]
        ],
        **kwargs: Any
    ) -> _models.HybridRunbookWorkerGroup:
        """Create a hybrid runbook worker group.

        .. seealso::
           - http://aka.ms/azureautomationsdk/hybridrunbookworkergroupoperations

        :param resource_group_name: Name of an Azure Resource group. Required.
        :type resource_group_name: str
        :param automation_account_name: The name of the automation account. Required.
        :type automation_account_name: str
        :param hybrid_runbook_worker_group_name: The hybrid runbook worker group name. Required.
        :type hybrid_runbook_worker_group_name: str
        :param hybrid_runbook_worker_group_creation_parameters: The create or update parameters for
         hybrid runbook worker group. Is either a HybridRunbookWorkerGroupCreateOrUpdateParameters type
         or a IO[bytes] type. Required.
        :type hybrid_runbook_worker_group_creation_parameters:
         ~azure.mgmt.automation.models.HybridRunbookWorkerGroupCreateOrUpdateParameters or IO[bytes]
        :return: HybridRunbookWorkerGroup or the result of cls(response)
        :rtype: ~azure.mgmt.automation.models.HybridRunbookWorkerGroup
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map: MutableMapping[int, Type[HttpResponseError]] = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: str = kwargs.pop("api_version", _params.pop("api-version", "2022-08-08"))
        content_type: Optional[str] = kwargs.pop("content_type", _headers.pop("Content-Type", None))
        cls: ClsType[_models.HybridRunbookWorkerGroup] = kwargs.pop("cls", None)

        content_type = content_type or "application/json"
        _json = None
        _content = None
        if isinstance(hybrid_runbook_worker_group_creation_parameters, (IOBase, bytes)):
            _content = hybrid_runbook_worker_group_creation_parameters
        else:
            _json = self._serialize.body(
                hybrid_runbook_worker_group_creation_parameters, "HybridRunbookWorkerGroupCreateOrUpdateParameters"
            )

        _request = build_create_request(
            resource_group_name=resource_group_name,
            automation_account_name=automation_account_name,
            hybrid_runbook_worker_group_name=hybrid_runbook_worker_group_name,
            subscription_id=self._config.subscription_id,
            api_version=api_version,
            content_type=content_type,
            json=_json,
            content=_content,
            headers=_headers,
            params=_params,
        )
        _request.url = self._client.format_url(_request.url)

        _stream = False
        pipeline_response: PipelineResponse = self._client._pipeline.run(  # pylint: disable=protected-access
            _request, stream=_stream, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200, 201]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.ErrorResponse, pipeline_response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        deserialized = self._deserialize("HybridRunbookWorkerGroup", pipeline_response.http_response)

        if cls:
            return cls(pipeline_response, deserialized, {})  # type: ignore

        return deserialized  # type: ignore

    @overload
    def update(
        self,
        resource_group_name: str,
        automation_account_name: str,
        hybrid_runbook_worker_group_name: str,
        hybrid_runbook_worker_group_updation_parameters: _models.HybridRunbookWorkerGroupCreateOrUpdateParameters,
        *,
        content_type: str = "application/json",
        **kwargs: Any
    ) -> _models.HybridRunbookWorkerGroup:
        """Update a hybrid runbook worker group.

        .. seealso::
           - http://aka.ms/azureautomationsdk/hybridrunbookworkergroupoperations

        :param resource_group_name: Name of an Azure Resource group. Required.
        :type resource_group_name: str
        :param automation_account_name: The name of the automation account. Required.
        :type automation_account_name: str
        :param hybrid_runbook_worker_group_name: The hybrid runbook worker group name. Required.
        :type hybrid_runbook_worker_group_name: str
        :param hybrid_runbook_worker_group_updation_parameters: The hybrid runbook worker group.
         Required.
        :type hybrid_runbook_worker_group_updation_parameters:
         ~azure.mgmt.automation.models.HybridRunbookWorkerGroupCreateOrUpdateParameters
        :keyword content_type: Body Parameter content-type. Content type parameter for JSON body.
         Default value is "application/json".
        :paramtype content_type: str
        :return: HybridRunbookWorkerGroup or the result of cls(response)
        :rtype: ~azure.mgmt.automation.models.HybridRunbookWorkerGroup
        :raises ~azure.core.exceptions.HttpResponseError:
        """

    @overload
    def update(
        self,
        resource_group_name: str,
        automation_account_name: str,
        hybrid_runbook_worker_group_name: str,
        hybrid_runbook_worker_group_updation_parameters: IO[bytes],
        *,
        content_type: str = "application/json",
        **kwargs: Any
    ) -> _models.HybridRunbookWorkerGroup:
        """Update a hybrid runbook worker group.

        .. seealso::
           - http://aka.ms/azureautomationsdk/hybridrunbookworkergroupoperations

        :param resource_group_name: Name of an Azure Resource group. Required.
        :type resource_group_name: str
        :param automation_account_name: The name of the automation account. Required.
        :type automation_account_name: str
        :param hybrid_runbook_worker_group_name: The hybrid runbook worker group name. Required.
        :type hybrid_runbook_worker_group_name: str
        :param hybrid_runbook_worker_group_updation_parameters: The hybrid runbook worker group.
         Required.
        :type hybrid_runbook_worker_group_updation_parameters: IO[bytes]
        :keyword content_type: Body Parameter content-type. Content type parameter for binary body.
         Default value is "application/json".
        :paramtype content_type: str
        :return: HybridRunbookWorkerGroup or the result of cls(response)
        :rtype: ~azure.mgmt.automation.models.HybridRunbookWorkerGroup
        :raises ~azure.core.exceptions.HttpResponseError:
        """

    @distributed_trace
    def update(
        self,
        resource_group_name: str,
        automation_account_name: str,
        hybrid_runbook_worker_group_name: str,
        hybrid_runbook_worker_group_updation_parameters: Union[
            _models.HybridRunbookWorkerGroupCreateOrUpdateParameters, IO[bytes]
        ],
        **kwargs: Any
    ) -> _models.HybridRunbookWorkerGroup:
        """Update a hybrid runbook worker group.

        .. seealso::
           - http://aka.ms/azureautomationsdk/hybridrunbookworkergroupoperations

        :param resource_group_name: Name of an Azure Resource group. Required.
        :type resource_group_name: str
        :param automation_account_name: The name of the automation account. Required.
        :type automation_account_name: str
        :param hybrid_runbook_worker_group_name: The hybrid runbook worker group name. Required.
        :type hybrid_runbook_worker_group_name: str
        :param hybrid_runbook_worker_group_updation_parameters: The hybrid runbook worker group. Is
         either a HybridRunbookWorkerGroupCreateOrUpdateParameters type or a IO[bytes] type. Required.
        :type hybrid_runbook_worker_group_updation_parameters:
         ~azure.mgmt.automation.models.HybridRunbookWorkerGroupCreateOrUpdateParameters or IO[bytes]
        :return: HybridRunbookWorkerGroup or the result of cls(response)
        :rtype: ~azure.mgmt.automation.models.HybridRunbookWorkerGroup
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map: MutableMapping[int, Type[HttpResponseError]] = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: str = kwargs.pop("api_version", _params.pop("api-version", "2022-08-08"))
        content_type: Optional[str] = kwargs.pop("content_type", _headers.pop("Content-Type", None))
        cls: ClsType[_models.HybridRunbookWorkerGroup] = kwargs.pop("cls", None)

        content_type = content_type or "application/json"
        _json = None
        _content = None
        if isinstance(hybrid_runbook_worker_group_updation_parameters, (IOBase, bytes)):
            _content = hybrid_runbook_worker_group_updation_parameters
        else:
            _json = self._serialize.body(
                hybrid_runbook_worker_group_updation_parameters, "HybridRunbookWorkerGroupCreateOrUpdateParameters"
            )

        _request = build_update_request(
            resource_group_name=resource_group_name,
            automation_account_name=automation_account_name,
            hybrid_runbook_worker_group_name=hybrid_runbook_worker_group_name,
            subscription_id=self._config.subscription_id,
            api_version=api_version,
            content_type=content_type,
            json=_json,
            content=_content,
            headers=_headers,
            params=_params,
        )
        _request.url = self._client.format_url(_request.url)

        _stream = False
        pipeline_response: PipelineResponse = self._client._pipeline.run(  # pylint: disable=protected-access
            _request, stream=_stream, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.ErrorResponse, pipeline_response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        deserialized = self._deserialize("HybridRunbookWorkerGroup", pipeline_response.http_response)

        if cls:
            return cls(pipeline_response, deserialized, {})  # type: ignore

        return deserialized  # type: ignore

    @distributed_trace
    def list_by_automation_account(
        self, resource_group_name: str, automation_account_name: str, filter: Optional[str] = None, **kwargs: Any
    ) -> Iterable["_models.HybridRunbookWorkerGroup"]:
        """Retrieve a list of hybrid runbook worker groups.

        .. seealso::
           - http://aka.ms/azureautomationsdk/hybridrunbookworkergroupoperations

        :param resource_group_name: Name of an Azure Resource group. Required.
        :type resource_group_name: str
        :param automation_account_name: The name of the automation account. Required.
        :type automation_account_name: str
        :param filter: The filter to apply on the operation. Default value is None.
        :type filter: str
        :return: An iterator like instance of either HybridRunbookWorkerGroup or the result of
         cls(response)
        :rtype: ~azure.core.paging.ItemPaged[~azure.mgmt.automation.models.HybridRunbookWorkerGroup]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: str = kwargs.pop("api_version", _params.pop("api-version", "2022-08-08"))
        cls: ClsType[_models.HybridRunbookWorkerGroupsListResult] = kwargs.pop("cls", None)

        error_map: MutableMapping[int, Type[HttpResponseError]] = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        def prepare_request(next_link=None):
            if not next_link:

                _request = build_list_by_automation_account_request(
                    resource_group_name=resource_group_name,
                    automation_account_name=automation_account_name,
                    subscription_id=self._config.subscription_id,
                    filter=filter,
                    api_version=api_version,
                    headers=_headers,
                    params=_params,
                )
                _request.url = self._client.format_url(_request.url)

            else:
                _request = HttpRequest("GET", next_link)
                _request.url = self._client.format_url(_request.url)
                _request.method = "GET"
            return _request

        def extract_data(pipeline_response):
            deserialized = self._deserialize("HybridRunbookWorkerGroupsListResult", pipeline_response)
            list_of_elem = deserialized.value
            if cls:
                list_of_elem = cls(list_of_elem)  # type: ignore
            return deserialized.next_link or None, iter(list_of_elem)

        def get_next(next_link=None):
            _request = prepare_request(next_link)

            _stream = False
            pipeline_response: PipelineResponse = self._client._pipeline.run(  # pylint: disable=protected-access
                _request, stream=_stream, **kwargs
            )
            response = pipeline_response.http_response

            if response.status_code not in [200]:
                map_error(status_code=response.status_code, response=response, error_map=error_map)
                error = self._deserialize.failsafe_deserialize(_models.ErrorResponse, pipeline_response)
                raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

            return pipeline_response

        return ItemPaged(get_next, extract_data)
