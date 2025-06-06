# pylint: disable=line-too-long,useless-suppression
# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
from collections.abc import MutableMapping
from typing import Any, AsyncIterable, Callable, Dict, Optional, TypeVar
import urllib.parse

from azure.core import AsyncPipelineClient
from azure.core.async_paging import AsyncItemPaged, AsyncList
from azure.core.exceptions import (
    ClientAuthenticationError,
    HttpResponseError,
    ResourceExistsError,
    ResourceNotFoundError,
    ResourceNotModifiedError,
    map_error,
)
from azure.core.pipeline import PipelineResponse
from azure.core.rest import AsyncHttpResponse, HttpRequest
from azure.core.tracing.decorator import distributed_trace
from azure.core.tracing.decorator_async import distributed_trace_async
from azure.core.utils import case_insensitive_dict
from azure.mgmt.core.exceptions import ARMErrorFormat

from ... import models as _models
from ..._utils.serialization import Deserializer, Serializer
from ...operations._extension_types_operations import (
    build_cluster_get_version_request,
    build_cluster_list_versions_request,
    build_get_request,
    build_get_version_request,
    build_list_request,
    build_list_versions_request,
    build_location_get_request,
    build_location_list_request,
)
from .._configuration import KubernetesConfigurationExtensionTypesMgmtClientConfiguration

T = TypeVar("T")
ClsType = Optional[Callable[[PipelineResponse[HttpRequest, AsyncHttpResponse], T, Dict[str, Any]], Any]]


class ExtensionTypesOperations:
    """
    .. warning::
        **DO NOT** instantiate this class directly.

        Instead, you should access the following operations through
        :class:`~azure.mgmt.kubernetesconfiguration.extensiontypes.aio.KubernetesConfigurationExtensionTypesMgmtClient`'s
        :attr:`extension_types` attribute.
    """

    models = _models

    def __init__(self, *args, **kwargs) -> None:
        input_args = list(args)
        self._client: AsyncPipelineClient = input_args.pop(0) if input_args else kwargs.pop("client")
        self._config: KubernetesConfigurationExtensionTypesMgmtClientConfiguration = (
            input_args.pop(0) if input_args else kwargs.pop("config")
        )
        self._serialize: Serializer = input_args.pop(0) if input_args else kwargs.pop("serializer")
        self._deserialize: Deserializer = input_args.pop(0) if input_args else kwargs.pop("deserializer")

    @distributed_trace
    def location_list(
        self,
        location: str,
        publisher_id: Optional[str] = None,
        offer_id: Optional[str] = None,
        plan_id: Optional[str] = None,
        release_train: Optional[str] = None,
        cluster_type: Optional[str] = None,
        **kwargs: Any
    ) -> AsyncIterable["_models.ExtensionType"]:
        """List all Extension Types for the location.

        :param location: The name of Azure region. Required.
        :type location: str
        :param publisher_id: Filter results by Publisher ID of a marketplace extension type. Default
         value is None.
        :type publisher_id: str
        :param offer_id: Filter results by Offer or Product ID of a marketplace extension type. Default
         value is None.
        :type offer_id: str
        :param plan_id: Filter results by Plan ID of a marketplace extension type. Default value is
         None.
        :type plan_id: str
        :param release_train: Filter results by release train (default value is stable). Default value
         is None.
        :type release_train: str
        :param cluster_type: Filter results by the cluster type for extension types. Default value is
         None.
        :type cluster_type: str
        :return: An iterator like instance of either ExtensionType or the result of cls(response)
        :rtype:
         ~azure.core.async_paging.AsyncItemPaged[~azure.mgmt.kubernetesconfiguration.extensiontypes.models.ExtensionType]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: str = kwargs.pop("api_version", _params.pop("api-version", self._config.api_version))
        cls: ClsType[_models.ExtensionTypesList] = kwargs.pop("cls", None)

        error_map: MutableMapping = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        def prepare_request(next_link=None):
            if not next_link:

                _request = build_location_list_request(
                    location=location,
                    subscription_id=self._config.subscription_id,
                    publisher_id=publisher_id,
                    offer_id=offer_id,
                    plan_id=plan_id,
                    release_train=release_train,
                    cluster_type=cluster_type,
                    api_version=api_version,
                    headers=_headers,
                    params=_params,
                )
                _request.url = self._client.format_url(_request.url)

            else:
                # make call to next link with the client's api-version
                _parsed_next_link = urllib.parse.urlparse(next_link)
                _next_request_params = case_insensitive_dict(
                    {
                        key: [urllib.parse.quote(v) for v in value]
                        for key, value in urllib.parse.parse_qs(_parsed_next_link.query).items()
                    }
                )
                _next_request_params["api-version"] = self._config.api_version
                _request = HttpRequest(
                    "GET", urllib.parse.urljoin(next_link, _parsed_next_link.path), params=_next_request_params
                )
                _request.url = self._client.format_url(_request.url)
                _request.method = "GET"
            return _request

        async def extract_data(pipeline_response):
            deserialized = self._deserialize("ExtensionTypesList", pipeline_response)
            list_of_elem = deserialized.value
            if cls:
                list_of_elem = cls(list_of_elem)  # type: ignore
            return deserialized.next_link or None, AsyncList(list_of_elem)

        async def get_next(next_link=None):
            _request = prepare_request(next_link)

            _stream = False
            pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
                _request, stream=_stream, **kwargs
            )
            response = pipeline_response.http_response

            if response.status_code not in [200]:
                map_error(status_code=response.status_code, response=response, error_map=error_map)
                error = self._deserialize.failsafe_deserialize(_models.ErrorResponse, pipeline_response)
                raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

            return pipeline_response

        return AsyncItemPaged(get_next, extract_data)

    @distributed_trace_async
    async def location_get(self, location: str, extension_type_name: str, **kwargs: Any) -> _models.ExtensionType:
        """Get an extension type for the location.

        :param location: The name of Azure region. Required.
        :type location: str
        :param extension_type_name: Name of the Extension Type. Required.
        :type extension_type_name: str
        :return: ExtensionType or the result of cls(response)
        :rtype: ~azure.mgmt.kubernetesconfiguration.extensiontypes.models.ExtensionType
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
        cls: ClsType[_models.ExtensionType] = kwargs.pop("cls", None)

        _request = build_location_get_request(
            location=location,
            extension_type_name=extension_type_name,
            subscription_id=self._config.subscription_id,
            api_version=api_version,
            headers=_headers,
            params=_params,
        )
        _request.url = self._client.format_url(_request.url)

        _stream = False
        pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
            _request, stream=_stream, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.ErrorResponse, pipeline_response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        deserialized = self._deserialize("ExtensionType", pipeline_response.http_response)

        if cls:
            return cls(pipeline_response, deserialized, {})  # type: ignore

        return deserialized  # type: ignore

    @distributed_trace
    def list_versions(
        self,
        location: str,
        extension_type_name: str,
        release_train: Optional[str] = None,
        cluster_type: Optional[str] = None,
        major_version: Optional[str] = None,
        show_latest: Optional[bool] = None,
        **kwargs: Any
    ) -> AsyncIterable["_models.ExtensionTypeVersionForReleaseTrain"]:
        """List the versions for an extension type and location.

        :param location: The name of Azure region. Required.
        :type location: str
        :param extension_type_name: Name of the Extension Type. Required.
        :type extension_type_name: str
        :param release_train: Filter results by release train (default value is stable). Default value
         is None.
        :type release_train: str
        :param cluster_type: Filter results by the cluster type for extension types. Default value is
         None.
        :type cluster_type: str
        :param major_version: Filter results by the major version of an extension type. Default value
         is None.
        :type major_version: str
        :param show_latest: Filter results by only the latest version (based on other query
         parameters). Default value is None.
        :type show_latest: bool
        :return: An iterator like instance of either ExtensionTypeVersionForReleaseTrain or the result
         of cls(response)
        :rtype:
         ~azure.core.async_paging.AsyncItemPaged[~azure.mgmt.kubernetesconfiguration.extensiontypes.models.ExtensionTypeVersionForReleaseTrain]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: str = kwargs.pop("api_version", _params.pop("api-version", self._config.api_version))
        cls: ClsType[_models.ExtensionTypeVersionsList] = kwargs.pop("cls", None)

        error_map: MutableMapping = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        def prepare_request(next_link=None):
            if not next_link:

                _request = build_list_versions_request(
                    location=location,
                    extension_type_name=extension_type_name,
                    subscription_id=self._config.subscription_id,
                    release_train=release_train,
                    cluster_type=cluster_type,
                    major_version=major_version,
                    show_latest=show_latest,
                    api_version=api_version,
                    headers=_headers,
                    params=_params,
                )
                _request.url = self._client.format_url(_request.url)

            else:
                # make call to next link with the client's api-version
                _parsed_next_link = urllib.parse.urlparse(next_link)
                _next_request_params = case_insensitive_dict(
                    {
                        key: [urllib.parse.quote(v) for v in value]
                        for key, value in urllib.parse.parse_qs(_parsed_next_link.query).items()
                    }
                )
                _next_request_params["api-version"] = self._config.api_version
                _request = HttpRequest(
                    "GET", urllib.parse.urljoin(next_link, _parsed_next_link.path), params=_next_request_params
                )
                _request.url = self._client.format_url(_request.url)
                _request.method = "GET"
            return _request

        async def extract_data(pipeline_response):
            deserialized = self._deserialize("ExtensionTypeVersionsList", pipeline_response)
            list_of_elem = deserialized.value
            if cls:
                list_of_elem = cls(list_of_elem)  # type: ignore
            return deserialized.next_link or None, AsyncList(list_of_elem)

        async def get_next(next_link=None):
            _request = prepare_request(next_link)

            _stream = False
            pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
                _request, stream=_stream, **kwargs
            )
            response = pipeline_response.http_response

            if response.status_code not in [200]:
                map_error(status_code=response.status_code, response=response, error_map=error_map)
                error = self._deserialize.failsafe_deserialize(_models.ErrorResponse, pipeline_response)
                raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

            return pipeline_response

        return AsyncItemPaged(get_next, extract_data)

    @distributed_trace_async
    async def get_version(
        self, location: str, extension_type_name: str, version_number: str, **kwargs: Any
    ) -> _models.ExtensionTypeVersionForReleaseTrain:
        """Get details of a version for an extension type and location.

        :param location: The name of Azure region. Required.
        :type location: str
        :param extension_type_name: Name of the Extension Type. Required.
        :type extension_type_name: str
        :param version_number: Version number of the Extension Type. Required.
        :type version_number: str
        :return: ExtensionTypeVersionForReleaseTrain or the result of cls(response)
        :rtype:
         ~azure.mgmt.kubernetesconfiguration.extensiontypes.models.ExtensionTypeVersionForReleaseTrain
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
        cls: ClsType[_models.ExtensionTypeVersionForReleaseTrain] = kwargs.pop("cls", None)

        _request = build_get_version_request(
            location=location,
            extension_type_name=extension_type_name,
            version_number=version_number,
            subscription_id=self._config.subscription_id,
            api_version=api_version,
            headers=_headers,
            params=_params,
        )
        _request.url = self._client.format_url(_request.url)

        _stream = False
        pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
            _request, stream=_stream, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.ErrorResponse, pipeline_response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        deserialized = self._deserialize("ExtensionTypeVersionForReleaseTrain", pipeline_response.http_response)

        if cls:
            return cls(pipeline_response, deserialized, {})  # type: ignore

        return deserialized  # type: ignore

    @distributed_trace
    def list(
        self,
        resource_group_name: str,
        cluster_rp: str,
        cluster_resource_name: str,
        cluster_name: str,
        publisher_id: Optional[str] = None,
        offer_id: Optional[str] = None,
        plan_id: Optional[str] = None,
        release_train: Optional[str] = None,
        **kwargs: Any
    ) -> AsyncIterable["_models.ExtensionType"]:
        """List installable Extension Types for the cluster based region and type for the cluster.

        :param resource_group_name: The name of the resource group. The name is case insensitive.
         Required.
        :type resource_group_name: str
        :param cluster_rp: The Kubernetes cluster RP - i.e. Microsoft.ContainerService,
         Microsoft.Kubernetes, Microsoft.HybridContainerService. Required.
        :type cluster_rp: str
        :param cluster_resource_name: The Kubernetes cluster resource name - i.e. managedClusters,
         connectedClusters, provisionedClusters, appliances. Required.
        :type cluster_resource_name: str
        :param cluster_name: The name of the kubernetes cluster. Required.
        :type cluster_name: str
        :param publisher_id: Filter results by Publisher ID of a marketplace extension type. Default
         value is None.
        :type publisher_id: str
        :param offer_id: Filter results by Offer or Product ID of a marketplace extension type. Default
         value is None.
        :type offer_id: str
        :param plan_id: Filter results by Plan ID of a marketplace extension type. Default value is
         None.
        :type plan_id: str
        :param release_train: Filter results by release train (default value is stable). Default value
         is None.
        :type release_train: str
        :return: An iterator like instance of either ExtensionType or the result of cls(response)
        :rtype:
         ~azure.core.async_paging.AsyncItemPaged[~azure.mgmt.kubernetesconfiguration.extensiontypes.models.ExtensionType]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: str = kwargs.pop("api_version", _params.pop("api-version", self._config.api_version))
        cls: ClsType[_models.ExtensionTypesList] = kwargs.pop("cls", None)

        error_map: MutableMapping = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        def prepare_request(next_link=None):
            if not next_link:

                _request = build_list_request(
                    resource_group_name=resource_group_name,
                    cluster_rp=cluster_rp,
                    cluster_resource_name=cluster_resource_name,
                    cluster_name=cluster_name,
                    subscription_id=self._config.subscription_id,
                    publisher_id=publisher_id,
                    offer_id=offer_id,
                    plan_id=plan_id,
                    release_train=release_train,
                    api_version=api_version,
                    headers=_headers,
                    params=_params,
                )
                _request.url = self._client.format_url(_request.url)

            else:
                # make call to next link with the client's api-version
                _parsed_next_link = urllib.parse.urlparse(next_link)
                _next_request_params = case_insensitive_dict(
                    {
                        key: [urllib.parse.quote(v) for v in value]
                        for key, value in urllib.parse.parse_qs(_parsed_next_link.query).items()
                    }
                )
                _next_request_params["api-version"] = self._config.api_version
                _request = HttpRequest(
                    "GET", urllib.parse.urljoin(next_link, _parsed_next_link.path), params=_next_request_params
                )
                _request.url = self._client.format_url(_request.url)
                _request.method = "GET"
            return _request

        async def extract_data(pipeline_response):
            deserialized = self._deserialize("ExtensionTypesList", pipeline_response)
            list_of_elem = deserialized.value
            if cls:
                list_of_elem = cls(list_of_elem)  # type: ignore
            return deserialized.next_link or None, AsyncList(list_of_elem)

        async def get_next(next_link=None):
            _request = prepare_request(next_link)

            _stream = False
            pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
                _request, stream=_stream, **kwargs
            )
            response = pipeline_response.http_response

            if response.status_code not in [200]:
                map_error(status_code=response.status_code, response=response, error_map=error_map)
                error = self._deserialize.failsafe_deserialize(_models.ErrorResponse, pipeline_response)
                raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

            return pipeline_response

        return AsyncItemPaged(get_next, extract_data)

    @distributed_trace_async
    async def get(
        self,
        resource_group_name: str,
        cluster_rp: str,
        cluster_resource_name: str,
        cluster_name: str,
        extension_type_name: str,
        **kwargs: Any
    ) -> _models.ExtensionType:
        """Get an Extension Type installable to the cluster based region and type for the cluster.

        :param resource_group_name: The name of the resource group. The name is case insensitive.
         Required.
        :type resource_group_name: str
        :param cluster_rp: The Kubernetes cluster RP - i.e. Microsoft.ContainerService,
         Microsoft.Kubernetes, Microsoft.HybridContainerService. Required.
        :type cluster_rp: str
        :param cluster_resource_name: The Kubernetes cluster resource name - i.e. managedClusters,
         connectedClusters, provisionedClusters, appliances. Required.
        :type cluster_resource_name: str
        :param cluster_name: The name of the kubernetes cluster. Required.
        :type cluster_name: str
        :param extension_type_name: Name of the Extension Type. Required.
        :type extension_type_name: str
        :return: ExtensionType or the result of cls(response)
        :rtype: ~azure.mgmt.kubernetesconfiguration.extensiontypes.models.ExtensionType
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
        cls: ClsType[_models.ExtensionType] = kwargs.pop("cls", None)

        _request = build_get_request(
            resource_group_name=resource_group_name,
            cluster_rp=cluster_rp,
            cluster_resource_name=cluster_resource_name,
            cluster_name=cluster_name,
            extension_type_name=extension_type_name,
            subscription_id=self._config.subscription_id,
            api_version=api_version,
            headers=_headers,
            params=_params,
        )
        _request.url = self._client.format_url(_request.url)

        _stream = False
        pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
            _request, stream=_stream, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.ErrorResponse, pipeline_response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        deserialized = self._deserialize("ExtensionType", pipeline_response.http_response)

        if cls:
            return cls(pipeline_response, deserialized, {})  # type: ignore

        return deserialized  # type: ignore

    @distributed_trace
    def cluster_list_versions(
        self,
        resource_group_name: str,
        cluster_rp: str,
        cluster_resource_name: str,
        cluster_name: str,
        extension_type_name: str,
        release_train: Optional[str] = None,
        major_version: Optional[str] = None,
        show_latest: Optional[bool] = None,
        **kwargs: Any
    ) -> AsyncIterable["_models.ExtensionTypeVersionForReleaseTrain"]:
        """List the version for an Extension Type installable to the cluster.

        :param resource_group_name: The name of the resource group. The name is case insensitive.
         Required.
        :type resource_group_name: str
        :param cluster_rp: The Kubernetes cluster RP - i.e. Microsoft.ContainerService,
         Microsoft.Kubernetes, Microsoft.HybridContainerService. Required.
        :type cluster_rp: str
        :param cluster_resource_name: The Kubernetes cluster resource name - i.e. managedClusters,
         connectedClusters, provisionedClusters, appliances. Required.
        :type cluster_resource_name: str
        :param cluster_name: The name of the kubernetes cluster. Required.
        :type cluster_name: str
        :param extension_type_name: Name of the Extension Type. Required.
        :type extension_type_name: str
        :param release_train: Filter results by release train (default value is stable). Default value
         is None.
        :type release_train: str
        :param major_version: Filter results by the major version of an extension type. Default value
         is None.
        :type major_version: str
        :param show_latest: Filter results by only the latest version (based on other query
         parameters). Default value is None.
        :type show_latest: bool
        :return: An iterator like instance of either ExtensionTypeVersionForReleaseTrain or the result
         of cls(response)
        :rtype:
         ~azure.core.async_paging.AsyncItemPaged[~azure.mgmt.kubernetesconfiguration.extensiontypes.models.ExtensionTypeVersionForReleaseTrain]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: str = kwargs.pop("api_version", _params.pop("api-version", self._config.api_version))
        cls: ClsType[_models.ExtensionTypeVersionsList] = kwargs.pop("cls", None)

        error_map: MutableMapping = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        def prepare_request(next_link=None):
            if not next_link:

                _request = build_cluster_list_versions_request(
                    resource_group_name=resource_group_name,
                    cluster_rp=cluster_rp,
                    cluster_resource_name=cluster_resource_name,
                    cluster_name=cluster_name,
                    extension_type_name=extension_type_name,
                    subscription_id=self._config.subscription_id,
                    release_train=release_train,
                    major_version=major_version,
                    show_latest=show_latest,
                    api_version=api_version,
                    headers=_headers,
                    params=_params,
                )
                _request.url = self._client.format_url(_request.url)

            else:
                # make call to next link with the client's api-version
                _parsed_next_link = urllib.parse.urlparse(next_link)
                _next_request_params = case_insensitive_dict(
                    {
                        key: [urllib.parse.quote(v) for v in value]
                        for key, value in urllib.parse.parse_qs(_parsed_next_link.query).items()
                    }
                )
                _next_request_params["api-version"] = self._config.api_version
                _request = HttpRequest(
                    "GET", urllib.parse.urljoin(next_link, _parsed_next_link.path), params=_next_request_params
                )
                _request.url = self._client.format_url(_request.url)
                _request.method = "GET"
            return _request

        async def extract_data(pipeline_response):
            deserialized = self._deserialize("ExtensionTypeVersionsList", pipeline_response)
            list_of_elem = deserialized.value
            if cls:
                list_of_elem = cls(list_of_elem)  # type: ignore
            return deserialized.next_link or None, AsyncList(list_of_elem)

        async def get_next(next_link=None):
            _request = prepare_request(next_link)

            _stream = False
            pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
                _request, stream=_stream, **kwargs
            )
            response = pipeline_response.http_response

            if response.status_code not in [200]:
                map_error(status_code=response.status_code, response=response, error_map=error_map)
                error = self._deserialize.failsafe_deserialize(_models.ErrorResponse, pipeline_response)
                raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

            return pipeline_response

        return AsyncItemPaged(get_next, extract_data)

    @distributed_trace_async
    async def cluster_get_version(
        self,
        resource_group_name: str,
        cluster_rp: str,
        cluster_resource_name: str,
        cluster_name: str,
        extension_type_name: str,
        version_number: str,
        **kwargs: Any
    ) -> _models.ExtensionTypeVersionForReleaseTrain:
        """Get details of a version for an Extension Type installable to the cluster.

        :param resource_group_name: The name of the resource group. The name is case insensitive.
         Required.
        :type resource_group_name: str
        :param cluster_rp: The Kubernetes cluster RP - i.e. Microsoft.ContainerService,
         Microsoft.Kubernetes, Microsoft.HybridContainerService. Required.
        :type cluster_rp: str
        :param cluster_resource_name: The Kubernetes cluster resource name - i.e. managedClusters,
         connectedClusters, provisionedClusters, appliances. Required.
        :type cluster_resource_name: str
        :param cluster_name: The name of the kubernetes cluster. Required.
        :type cluster_name: str
        :param extension_type_name: Name of the Extension Type. Required.
        :type extension_type_name: str
        :param version_number: Version number of the Extension Type. Required.
        :type version_number: str
        :return: ExtensionTypeVersionForReleaseTrain or the result of cls(response)
        :rtype:
         ~azure.mgmt.kubernetesconfiguration.extensiontypes.models.ExtensionTypeVersionForReleaseTrain
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
        cls: ClsType[_models.ExtensionTypeVersionForReleaseTrain] = kwargs.pop("cls", None)

        _request = build_cluster_get_version_request(
            resource_group_name=resource_group_name,
            cluster_rp=cluster_rp,
            cluster_resource_name=cluster_resource_name,
            cluster_name=cluster_name,
            extension_type_name=extension_type_name,
            version_number=version_number,
            subscription_id=self._config.subscription_id,
            api_version=api_version,
            headers=_headers,
            params=_params,
        )
        _request.url = self._client.format_url(_request.url)

        _stream = False
        pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
            _request, stream=_stream, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.ErrorResponse, pipeline_response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        deserialized = self._deserialize("ExtensionTypeVersionForReleaseTrain", pipeline_response.http_response)

        if cls:
            return cls(pipeline_response, deserialized, {})  # type: ignore

        return deserialized  # type: ignore
