# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
from io import IOBase
import sys
from typing import Any, Callable, Dict, IO, Optional, TypeVar, Union, overload

from azure.core.exceptions import (
    ClientAuthenticationError,
    HttpResponseError,
    ResourceExistsError,
    ResourceNotFoundError,
    ResourceNotModifiedError,
    map_error,
)
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
    from typing import MutableMapping  # type: ignore
T = TypeVar("T")
ClsType = Optional[Callable[[PipelineResponse[HttpRequest, HttpResponse], T, Dict[str, Any]], Any]]

_SERIALIZER = Serializer()
_SERIALIZER.client_side_validation = False


def build_list_by_service_request(
    resource_group_name: str, service_name: str, quota_counter_key: str, subscription_id: str, **kwargs: Any
) -> HttpRequest:
    _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
    _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

    api_version: str = kwargs.pop("api_version", _params.pop("api-version", "2024-05-01"))
    accept = _headers.pop("Accept", "application/json")

    # Construct URL
    _url = kwargs.pop(
        "template_url",
        "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ApiManagement/service/{serviceName}/quotas/{quotaCounterKey}",
    )  # pylint: disable=line-too-long
    path_format_arguments = {
        "resourceGroupName": _SERIALIZER.url(
            "resource_group_name", resource_group_name, "str", max_length=90, min_length=1
        ),
        "serviceName": _SERIALIZER.url(
            "service_name",
            service_name,
            "str",
            max_length=50,
            min_length=1,
            pattern=r"^[a-zA-Z](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?$",
        ),
        "quotaCounterKey": _SERIALIZER.url("quota_counter_key", quota_counter_key, "str"),
        "subscriptionId": _SERIALIZER.url("subscription_id", subscription_id, "str"),
    }

    _url: str = _url.format(**path_format_arguments)  # type: ignore

    # Construct parameters
    _params["api-version"] = _SERIALIZER.query("api_version", api_version, "str")

    # Construct headers
    _headers["Accept"] = _SERIALIZER.header("accept", accept, "str")

    return HttpRequest(method="GET", url=_url, params=_params, headers=_headers, **kwargs)


def build_update_request(
    resource_group_name: str, service_name: str, quota_counter_key: str, subscription_id: str, **kwargs: Any
) -> HttpRequest:
    _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
    _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

    api_version: str = kwargs.pop("api_version", _params.pop("api-version", "2024-05-01"))
    content_type: Optional[str] = kwargs.pop("content_type", _headers.pop("Content-Type", None))
    accept = _headers.pop("Accept", "application/json")

    # Construct URL
    _url = kwargs.pop(
        "template_url",
        "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ApiManagement/service/{serviceName}/quotas/{quotaCounterKey}",
    )  # pylint: disable=line-too-long
    path_format_arguments = {
        "resourceGroupName": _SERIALIZER.url(
            "resource_group_name", resource_group_name, "str", max_length=90, min_length=1
        ),
        "serviceName": _SERIALIZER.url(
            "service_name",
            service_name,
            "str",
            max_length=50,
            min_length=1,
            pattern=r"^[a-zA-Z](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?$",
        ),
        "quotaCounterKey": _SERIALIZER.url("quota_counter_key", quota_counter_key, "str"),
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


class QuotaByCounterKeysOperations:
    """
    .. warning::
        **DO NOT** instantiate this class directly.

        Instead, you should access the following operations through
        :class:`~azure.mgmt.apimanagement.ApiManagementClient`'s
        :attr:`quota_by_counter_keys` attribute.
    """

    models = _models

    def __init__(self, *args, **kwargs):
        input_args = list(args)
        self._client = input_args.pop(0) if input_args else kwargs.pop("client")
        self._config = input_args.pop(0) if input_args else kwargs.pop("config")
        self._serialize = input_args.pop(0) if input_args else kwargs.pop("serializer")
        self._deserialize = input_args.pop(0) if input_args else kwargs.pop("deserializer")

    @distributed_trace
    def list_by_service(
        self, resource_group_name: str, service_name: str, quota_counter_key: str, **kwargs: Any
    ) -> _models.QuotaCounterCollection:
        """Lists a collection of current quota counter periods associated with the counter-key configured
        in the policy on the specified service instance. The api does not support paging yet.

        .. seealso::
           -
        https://docs.microsoft.com/en-us/azure/api-management/api-management-howto-product-with-rules#a-namepolicies-ato-configure-call-rate-limit-and-quota-policies

        :param resource_group_name: The name of the resource group. The name is case insensitive.
         Required.
        :type resource_group_name: str
        :param service_name: The name of the API Management service. Required.
        :type service_name: str
        :param quota_counter_key: Quota counter key identifier.This is the result of expression defined
         in counter-key attribute of the quota-by-key policy.For Example, if you specify
         counter-key="boo" in the policy, then it’s accessible by "boo" counter key. But if it’s defined
         as counter-key="@("b"+"a")" then it will be accessible by "ba" key. Required.
        :type quota_counter_key: str
        :return: QuotaCounterCollection or the result of cls(response)
        :rtype: ~azure.mgmt.apimanagement.models.QuotaCounterCollection
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map: MutableMapping = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: str = kwargs.pop("api_version", _params.pop("api-version", self._config.api_version))
        cls: ClsType[_models.QuotaCounterCollection] = kwargs.pop("cls", None)

        _request = build_list_by_service_request(
            resource_group_name=resource_group_name,
            service_name=service_name,
            quota_counter_key=quota_counter_key,
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

        deserialized = self._deserialize("QuotaCounterCollection", pipeline_response.http_response)

        if cls:
            return cls(pipeline_response, deserialized, {})  # type: ignore

        return deserialized  # type: ignore

    @overload
    def update(
        self,
        resource_group_name: str,
        service_name: str,
        quota_counter_key: str,
        parameters: _models.QuotaCounterValueUpdateContract,
        *,
        content_type: str = "application/json",
        **kwargs: Any
    ) -> _models.QuotaCounterCollection:
        """Updates all the quota counter values specified with the existing quota counter key to a value
        in the specified service instance. This should be used for reset of the quota counter values.

        :param resource_group_name: The name of the resource group. The name is case insensitive.
         Required.
        :type resource_group_name: str
        :param service_name: The name of the API Management service. Required.
        :type service_name: str
        :param quota_counter_key: Quota counter key identifier.This is the result of expression defined
         in counter-key attribute of the quota-by-key policy.For Example, if you specify
         counter-key="boo" in the policy, then it’s accessible by "boo" counter key. But if it’s defined
         as counter-key="@("b"+"a")" then it will be accessible by "ba" key. Required.
        :type quota_counter_key: str
        :param parameters: The value of the quota counter to be applied to all quota counter periods.
         Required.
        :type parameters: ~azure.mgmt.apimanagement.models.QuotaCounterValueUpdateContract
        :keyword content_type: Body Parameter content-type. Content type parameter for JSON body.
         Default value is "application/json".
        :paramtype content_type: str
        :return: QuotaCounterCollection or the result of cls(response)
        :rtype: ~azure.mgmt.apimanagement.models.QuotaCounterCollection
        :raises ~azure.core.exceptions.HttpResponseError:
        """

    @overload
    def update(
        self,
        resource_group_name: str,
        service_name: str,
        quota_counter_key: str,
        parameters: IO[bytes],
        *,
        content_type: str = "application/json",
        **kwargs: Any
    ) -> _models.QuotaCounterCollection:
        """Updates all the quota counter values specified with the existing quota counter key to a value
        in the specified service instance. This should be used for reset of the quota counter values.

        :param resource_group_name: The name of the resource group. The name is case insensitive.
         Required.
        :type resource_group_name: str
        :param service_name: The name of the API Management service. Required.
        :type service_name: str
        :param quota_counter_key: Quota counter key identifier.This is the result of expression defined
         in counter-key attribute of the quota-by-key policy.For Example, if you specify
         counter-key="boo" in the policy, then it’s accessible by "boo" counter key. But if it’s defined
         as counter-key="@("b"+"a")" then it will be accessible by "ba" key. Required.
        :type quota_counter_key: str
        :param parameters: The value of the quota counter to be applied to all quota counter periods.
         Required.
        :type parameters: IO[bytes]
        :keyword content_type: Body Parameter content-type. Content type parameter for binary body.
         Default value is "application/json".
        :paramtype content_type: str
        :return: QuotaCounterCollection or the result of cls(response)
        :rtype: ~azure.mgmt.apimanagement.models.QuotaCounterCollection
        :raises ~azure.core.exceptions.HttpResponseError:
        """

    @distributed_trace
    def update(
        self,
        resource_group_name: str,
        service_name: str,
        quota_counter_key: str,
        parameters: Union[_models.QuotaCounterValueUpdateContract, IO[bytes]],
        **kwargs: Any
    ) -> _models.QuotaCounterCollection:
        """Updates all the quota counter values specified with the existing quota counter key to a value
        in the specified service instance. This should be used for reset of the quota counter values.

        :param resource_group_name: The name of the resource group. The name is case insensitive.
         Required.
        :type resource_group_name: str
        :param service_name: The name of the API Management service. Required.
        :type service_name: str
        :param quota_counter_key: Quota counter key identifier.This is the result of expression defined
         in counter-key attribute of the quota-by-key policy.For Example, if you specify
         counter-key="boo" in the policy, then it’s accessible by "boo" counter key. But if it’s defined
         as counter-key="@("b"+"a")" then it will be accessible by "ba" key. Required.
        :type quota_counter_key: str
        :param parameters: The value of the quota counter to be applied to all quota counter periods.
         Is either a QuotaCounterValueUpdateContract type or a IO[bytes] type. Required.
        :type parameters: ~azure.mgmt.apimanagement.models.QuotaCounterValueUpdateContract or IO[bytes]
        :return: QuotaCounterCollection or the result of cls(response)
        :rtype: ~azure.mgmt.apimanagement.models.QuotaCounterCollection
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map: MutableMapping = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: str = kwargs.pop("api_version", _params.pop("api-version", self._config.api_version))
        content_type: Optional[str] = kwargs.pop("content_type", _headers.pop("Content-Type", None))
        cls: ClsType[_models.QuotaCounterCollection] = kwargs.pop("cls", None)

        content_type = content_type or "application/json"
        _json = None
        _content = None
        if isinstance(parameters, (IOBase, bytes)):
            _content = parameters
        else:
            _json = self._serialize.body(parameters, "QuotaCounterValueUpdateContract")

        _request = build_update_request(
            resource_group_name=resource_group_name,
            service_name=service_name,
            quota_counter_key=quota_counter_key,
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

        deserialized = self._deserialize("QuotaCounterCollection", pipeline_response.http_response)

        if cls:
            return cls(pipeline_response, deserialized, {})  # type: ignore

        return deserialized  # type: ignore
