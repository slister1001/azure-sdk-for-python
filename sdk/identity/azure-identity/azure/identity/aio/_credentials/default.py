# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
import logging
import os
from typing import List, Optional, Any, cast

from azure.core.credentials import AccessToken, AccessTokenInfo, TokenRequestOptions
from azure.core.credentials_async import AsyncTokenCredential, AsyncSupportsTokenInfo
from ..._constants import EnvironmentVariables
from ..._internal import get_default_authority, normalize_authority, within_dac, process_credential_exclusions
from .azure_cli import AzureCliCredential
from .azd_cli import AzureDeveloperCliCredential
from .azure_powershell import AzurePowerShellCredential
from .chained import ChainedTokenCredential
from .environment import EnvironmentCredential
from .managed_identity import ManagedIdentityCredential
from .shared_cache import SharedTokenCacheCredential
from .vscode import VisualStudioCodeCredential
from .workload_identity import WorkloadIdentityCredential


_LOGGER = logging.getLogger(__name__)


class DefaultAzureCredential(ChainedTokenCredential):
    """A credential capable of handling most Azure SDK authentication scenarios. See
    https://aka.ms/azsdk/python/identity/credential-chains#usage-guidance-for-defaultazurecredential.

    The identity it uses depends on the environment. When an access token is needed, it requests one using these
    identities in turn, stopping when one provides a token:

    1. A service principal configured by environment variables. See :class:`~azure.identity.aio.EnvironmentCredential`
       for more details.
    2. WorkloadIdentityCredential if environment variable configuration is set by the Azure workload
       identity webhook.
    3. An Azure managed identity. See :class:`~azure.identity.aio.ManagedIdentityCredential` for more details.
    4. On Windows only: a user who has signed in with a Microsoft application, such as Visual Studio. If multiple
       identities are in the cache, then the value of  the environment variable ``AZURE_USERNAME`` is used to select
       which identity to use. See :class:`~azure.identity.aio.SharedTokenCacheCredential` for more details.
    5. The identity currently logged in to the Azure CLI.
    6. The identity currently logged in to Azure PowerShell.
    7. The identity currently logged in to the Azure Developer CLI.

    This default behavior is configurable with keyword arguments.

    :keyword str authority: Authority of a Microsoft Entra endpoint, for example 'login.microsoftonline.com',
        the authority for Azure Public Cloud (which is the default). :class:`~azure.identity.AzureAuthorityHosts`
        defines authorities for other clouds. Managed identities ignore this because they reside in a single cloud.
    :keyword bool exclude_workload_identity_credential: Whether to exclude the workload identity from the credential.
        Defaults to **False**.
    :keyword bool exclude_developer_cli_credential: Whether to exclude the Azure Developer CLI
        from the credential. Defaults to **False**.
    :keyword bool exclude_cli_credential: Whether to exclude the Azure CLI from the credential. Defaults to **False**.
    :keyword bool exclude_environment_credential: Whether to exclude a service principal configured by environment
        variables from the credential. Defaults to **False**.
    :keyword bool exclude_powershell_credential: Whether to exclude Azure PowerShell. Defaults to **False**.
    :keyword bool exclude_visual_studio_code_credential: Whether to exclude stored credential from VS Code.
        Defaults to **True**.
    :keyword bool exclude_managed_identity_credential: Whether to exclude managed identity from the credential.
        Defaults to **False**.
    :keyword bool exclude_shared_token_cache_credential: Whether to exclude the shared token cache. Defaults to
        **False**.
    :keyword str managed_identity_client_id: The client ID of a user-assigned managed identity. Defaults to the value
        of the environment variable AZURE_CLIENT_ID, if any. If not specified, a system-assigned identity will be used.
    :keyword str workload_identity_client_id: The client ID of an identity assigned to the pod. Defaults to the value
        of the environment variable AZURE_CLIENT_ID, if any. If not specified, the pod's default identity will be used.
    :keyword str workload_identity_tenant_id: Preferred tenant for :class:`~azure.identity.WorkloadIdentityCredential`.
        Defaults to the value of environment variable AZURE_TENANT_ID, if any.
    :keyword str shared_cache_username: Preferred username for :class:`~azure.identity.aio.SharedTokenCacheCredential`.
        Defaults to the value of environment variable AZURE_USERNAME, if any.
    :keyword str shared_cache_tenant_id: Preferred tenant for :class:`~azure.identity.aio.SharedTokenCacheCredential`.
        Defaults to the value of environment variable AZURE_TENANT_ID, if any.
    :keyword str visual_studio_code_tenant_id: Tenant ID to use when authenticating with
        :class:`~azure.identity.VisualStudioCodeCredential`. Defaults to the tenant specified in the authentication
        record file used by the Azure Resources extension.
    :keyword int process_timeout: The timeout in seconds to use for developer credentials that run
        subprocesses (e.g. AzureCliCredential, AzurePowerShellCredential). Defaults to **10** seconds.

    .. admonition:: Example:

        .. literalinclude:: ../samples/credential_creation_code_snippets.py
            :start-after: [START create_default_credential_async]
            :end-before: [END create_default_credential_async]
            :language: python
            :dedent: 4
            :caption: Create a DefaultAzureCredential.
    """

    def __init__(self, **kwargs: Any) -> None:  # pylint: disable=too-many-statements, too-many-locals
        if "tenant_id" in kwargs:
            raise TypeError("'tenant_id' is not supported in DefaultAzureCredential.")

        authority = kwargs.pop("authority", None)
        authority = normalize_authority(authority) if authority else get_default_authority()

        vscode_tenant_id = kwargs.pop("visual_studio_code_tenant_id", None)

        shared_cache_username = kwargs.pop("shared_cache_username", os.environ.get(EnvironmentVariables.AZURE_USERNAME))
        shared_cache_tenant_id = kwargs.pop(
            "shared_cache_tenant_id", os.environ.get(EnvironmentVariables.AZURE_TENANT_ID)
        )

        managed_identity_client_id = kwargs.pop(
            "managed_identity_client_id", os.environ.get(EnvironmentVariables.AZURE_CLIENT_ID)
        )
        workload_identity_client_id = kwargs.pop("workload_identity_client_id", managed_identity_client_id)
        workload_identity_tenant_id = kwargs.pop(
            "workload_identity_tenant_id", os.environ.get(EnvironmentVariables.AZURE_TENANT_ID)
        )

        process_timeout = kwargs.pop("process_timeout", 10)

        # Define credential configuration mapping (async version)
        credential_config = {
            "environment": {
                "exclude_param": "exclude_environment_credential",
                "env_name": "environmentcredential",
                "default_exclude": False,
            },
            "workload_identity": {
                "exclude_param": "exclude_workload_identity_credential",
                "env_name": "workloadidentitycredential",
                "default_exclude": False,
            },
            "managed_identity": {
                "exclude_param": "exclude_managed_identity_credential",
                "env_name": "managedidentitycredential",
                "default_exclude": False,
            },
            "shared_token_cache": {
                "exclude_param": "exclude_shared_token_cache_credential",
                "default_exclude": False,
            },
            "visual_studio_code": {
                "exclude_param": "exclude_visual_studio_code_credential",
                "default_exclude": False,
            },
            "cli": {
                "exclude_param": "exclude_cli_credential",
                "env_name": "azureclicredential",
                "default_exclude": False,
            },
            "developer_cli": {
                "exclude_param": "exclude_developer_cli_credential",
                "env_name": "azuredeveloperclicredential",
                "default_exclude": False,
            },
            "powershell": {
                "exclude_param": "exclude_powershell_credential",
                "env_name": "azurepowershellcredential",
                "default_exclude": False,
            },
        }

        # Extract user-provided exclude flags and set defaults
        exclude_flags = {}
        user_excludes = {}
        for cred_key, config in credential_config.items():
            param_name = cast(str, config["exclude_param"])
            user_excludes[cred_key] = kwargs.pop(param_name, None)
            exclude_flags[cred_key] = config["default_exclude"]

        # Process AZURE_TOKEN_CREDENTIALS environment variable and apply user overrides
        exclude_flags = process_credential_exclusions(credential_config, exclude_flags, user_excludes)

        # Extract individual exclude flags for backward compatibility
        exclude_environment_credential = exclude_flags["environment"]
        exclude_workload_identity_credential = exclude_flags["workload_identity"]
        exclude_managed_identity_credential = exclude_flags["managed_identity"]
        exclude_shared_token_cache_credential = exclude_flags["shared_token_cache"]
        exclude_visual_studio_code_credential = exclude_flags["visual_studio_code"]
        exclude_cli_credential = exclude_flags["cli"]
        exclude_developer_cli_credential = exclude_flags["developer_cli"]
        exclude_powershell_credential = exclude_flags["powershell"]

        credentials: List[AsyncSupportsTokenInfo] = []
        within_dac.set(True)
        if not exclude_environment_credential:
            credentials.append(EnvironmentCredential(authority=authority, _within_dac=True, **kwargs))
        if not exclude_workload_identity_credential:
            if all(os.environ.get(var) for var in EnvironmentVariables.WORKLOAD_IDENTITY_VARS):
                client_id = workload_identity_client_id
                credentials.append(
                    WorkloadIdentityCredential(
                        client_id=cast(str, client_id),
                        tenant_id=workload_identity_tenant_id,
                        token_file_path=os.environ[EnvironmentVariables.AZURE_FEDERATED_TOKEN_FILE],
                        **kwargs,
                    )
                )
        if not exclude_managed_identity_credential:
            credentials.append(
                ManagedIdentityCredential(
                    client_id=managed_identity_client_id,
                    _exclude_workload_identity_credential=exclude_workload_identity_credential,
                    **kwargs,
                )
            )
        if not exclude_shared_token_cache_credential and SharedTokenCacheCredential.supported():
            try:
                # username and/or tenant_id are only required when the cache contains tokens for multiple identities
                shared_cache = SharedTokenCacheCredential(
                    username=shared_cache_username, tenant_id=shared_cache_tenant_id, authority=authority, **kwargs
                )
                credentials.append(shared_cache)
            except Exception as ex:  # pylint:disable=broad-except
                _LOGGER.info("Shared token cache is unavailable: '%s'", ex)
        if not exclude_visual_studio_code_credential:
            credentials.append(VisualStudioCodeCredential(tenant_id=vscode_tenant_id))
        if not exclude_cli_credential:
            credentials.append(AzureCliCredential(process_timeout=process_timeout))
        if not exclude_powershell_credential:
            credentials.append(AzurePowerShellCredential(process_timeout=process_timeout))
        if not exclude_developer_cli_credential:
            credentials.append(AzureDeveloperCliCredential(process_timeout=process_timeout))
        within_dac.set(False)
        super().__init__(*credentials)

    async def get_token(
        self, *scopes: str, claims: Optional[str] = None, tenant_id: Optional[str] = None, **kwargs: Any
    ) -> AccessToken:
        """Asynchronously request an access token for `scopes`.

        This method is called automatically by Azure SDK clients.

        :param str scopes: desired scopes for the access token. This method requires at least one scope.
            For more information about scopes, see
            https://learn.microsoft.com/entra/identity-platform/scopes-oidc.
        :keyword str claims: additional claims required in the token, such as those returned in a resource provider's
            claims challenge following an authorization failure.
        :keyword str tenant_id: optional tenant to include in the token request.

        :return: An access token with the desired scopes.
        :rtype: ~azure.core.credentials.AccessToken
        :raises ~azure.core.exceptions.ClientAuthenticationError: authentication failed. The exception has a
          `message` attribute listing each authentication attempt and its error message.
        """
        if self._successful_credential:
            token = await cast(AsyncTokenCredential, self._successful_credential).get_token(
                *scopes, claims=claims, tenant_id=tenant_id, **kwargs
            )
            _LOGGER.info(
                "%s acquired a token from %s", self.__class__.__name__, self._successful_credential.__class__.__name__
            )
            return token

        within_dac.set(True)
        token = await super().get_token(*scopes, claims=claims, tenant_id=tenant_id, **kwargs)
        within_dac.set(False)
        return token

    async def get_token_info(self, *scopes: str, options: Optional[TokenRequestOptions] = None) -> AccessTokenInfo:
        """Asynchronously request an access token for `scopes`.

        This is an alternative to `get_token` to enable certain scenarios that require additional properties
        on the token. This method is called automatically by Azure SDK clients.

        :param str scopes: desired scopes for the access token. This method requires at least one scope.
            For more information about scopes, see https://learn.microsoft.com/entra/identity-platform/scopes-oidc.
        :keyword options: A dictionary of options for the token request. Unknown options will be ignored. Optional.
        :paramtype options: ~azure.core.credentials.TokenRequestOptions

        :rtype: ~azure.core.credentials.AccessTokenInfo
        :return: An AccessTokenInfo instance containing information about the token.

        :raises ~azure.core.exceptions.ClientAuthenticationError: authentication failed. The exception has a
           `message` attribute listing each authentication attempt and its error message.
        """
        if self._successful_credential:
            token_info = await cast(AsyncSupportsTokenInfo, self._successful_credential).get_token_info(
                *scopes, options=options
            )
            _LOGGER.info(
                "%s acquired a token from %s", self.__class__.__name__, self._successful_credential.__class__.__name__
            )
            return token_info

        within_dac.set(True)
        token_info = await cast(AsyncSupportsTokenInfo, super()).get_token_info(*scopes, options=options)
        within_dac.set(False)
        return token_info
