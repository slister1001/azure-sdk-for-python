# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
from ._communication_identity_client import CommunicationIdentityClient
from ._generated.models import CommunicationTokenScope

from ._shared.models import (
    CommunicationCloudEnvironment,
    CommunicationIdentifier,
    CommunicationIdentifierKind,
    CommunicationUserIdentifier,
    CommunicationUserProperties,
    identifier_from_raw_id,
    MicrosoftTeamsAppIdentifier,
    MicrosoftTeamsAppProperties,
    MicrosoftTeamsUserIdentifier,
    MicrosoftTeamsUserProperties,
    PhoneNumberIdentifier,
    PhoneNumberProperties,
    UnknownIdentifier,
    TeamsExtensionUserIdentifier,
    TeamsExtensionUserProperties,
)

__all__ = [
    "CommunicationIdentityClient",
    # from _identity
    "CommunicationTokenScope",
    # from _shared
    "CommunicationCloudEnvironment",
    "CommunicationIdentifier",
    "CommunicationIdentifierKind",
    "CommunicationUserIdentifier",
    "CommunicationUserProperties",
    "identifier_from_raw_id",
    "MicrosoftTeamsAppIdentifier",
    "MicrosoftTeamsAppProperties",
    "MicrosoftTeamsUserIdentifier",
    "MicrosoftTeamsUserProperties",
    "PhoneNumberIdentifier",
    "PhoneNumberProperties",
    "UnknownIdentifier",
    "TeamsExtensionUserIdentifier",
    "TeamsExtensionUserProperties",
]
