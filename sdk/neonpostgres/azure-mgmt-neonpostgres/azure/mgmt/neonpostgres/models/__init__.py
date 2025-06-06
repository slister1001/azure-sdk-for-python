# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) Python Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
# pylint: disable=wrong-import-position

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ._patch import *  # pylint: disable=unused-wildcard-import


from ._models import (  # type: ignore
    Attributes,
    Branch,
    BranchProperties,
    CompanyDetails,
    Compute,
    ComputeProperties,
    ConnectionUriProperties,
    DefaultEndpointSettings,
    Endpoint,
    EndpointProperties,
    ErrorAdditionalInfo,
    ErrorDetail,
    ErrorResponse,
    MarketplaceDetails,
    NeonDatabase,
    NeonDatabaseProperties,
    NeonRole,
    NeonRoleProperties,
    OfferDetails,
    Operation,
    OperationDisplay,
    OrganizationProperties,
    OrganizationResource,
    PartnerOrganizationProperties,
    PgVersion,
    PgVersionsResult,
    Project,
    ProjectProperties,
    ProxyResource,
    Resource,
    SingleSignOnProperties,
    SystemData,
    TrackedResource,
    UserDetails,
)

from ._enums import (  # type: ignore
    ActionType,
    CreatedByType,
    EndpointType,
    MarketplaceSubscriptionStatus,
    Origin,
    ResourceProvisioningState,
    SingleSignOnStates,
)
from ._patch import __all__ as _patch_all
from ._patch import *
from ._patch import patch_sdk as _patch_sdk

__all__ = [
    "Attributes",
    "Branch",
    "BranchProperties",
    "CompanyDetails",
    "Compute",
    "ComputeProperties",
    "ConnectionUriProperties",
    "DefaultEndpointSettings",
    "Endpoint",
    "EndpointProperties",
    "ErrorAdditionalInfo",
    "ErrorDetail",
    "ErrorResponse",
    "MarketplaceDetails",
    "NeonDatabase",
    "NeonDatabaseProperties",
    "NeonRole",
    "NeonRoleProperties",
    "OfferDetails",
    "Operation",
    "OperationDisplay",
    "OrganizationProperties",
    "OrganizationResource",
    "PartnerOrganizationProperties",
    "PgVersion",
    "PgVersionsResult",
    "Project",
    "ProjectProperties",
    "ProxyResource",
    "Resource",
    "SingleSignOnProperties",
    "SystemData",
    "TrackedResource",
    "UserDetails",
    "ActionType",
    "CreatedByType",
    "EndpointType",
    "MarketplaceSubscriptionStatus",
    "Origin",
    "ResourceProvisioningState",
    "SingleSignOnStates",
]
__all__.extend([p for p in _patch_all if p not in __all__])  # pyright: ignore
_patch_sdk()
