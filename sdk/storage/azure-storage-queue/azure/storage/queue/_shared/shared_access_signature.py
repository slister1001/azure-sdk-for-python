# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from datetime import date

from .parser import _to_utc_datetime
from .constants import X_MS_VERSION
from . import sign_string, url_quote


# cspell:ignoreRegExp rsc.
# cspell:ignoreRegExp s..?id
class QueryStringConstants(object):
    SIGNED_SIGNATURE = "sig"
    SIGNED_PERMISSION = "sp"
    SIGNED_START = "st"
    SIGNED_EXPIRY = "se"
    SIGNED_RESOURCE = "sr"
    SIGNED_IDENTIFIER = "si"
    SIGNED_IP = "sip"
    SIGNED_PROTOCOL = "spr"
    SIGNED_VERSION = "sv"
    SIGNED_CACHE_CONTROL = "rscc"
    SIGNED_CONTENT_DISPOSITION = "rscd"
    SIGNED_CONTENT_ENCODING = "rsce"
    SIGNED_CONTENT_LANGUAGE = "rscl"
    SIGNED_CONTENT_TYPE = "rsct"
    START_PK = "spk"
    START_RK = "srk"
    END_PK = "epk"
    END_RK = "erk"
    SIGNED_RESOURCE_TYPES = "srt"
    SIGNED_SERVICES = "ss"
    SIGNED_OID = "skoid"
    SIGNED_TID = "sktid"
    SIGNED_KEY_START = "skt"
    SIGNED_KEY_EXPIRY = "ske"
    SIGNED_KEY_SERVICE = "sks"
    SIGNED_KEY_VERSION = "skv"
    SIGNED_ENCRYPTION_SCOPE = "ses"
    SIGNED_KEY_DELEGATED_USER_TID = "skdutid"
    SIGNED_DELEGATED_USER_OID = "sduoid"

    # for ADLS
    SIGNED_AUTHORIZED_OID = "saoid"
    SIGNED_UNAUTHORIZED_OID = "suoid"
    SIGNED_CORRELATION_ID = "scid"
    SIGNED_DIRECTORY_DEPTH = "sdd"

    @staticmethod
    def to_list():
        return [
            QueryStringConstants.SIGNED_SIGNATURE,
            QueryStringConstants.SIGNED_PERMISSION,
            QueryStringConstants.SIGNED_START,
            QueryStringConstants.SIGNED_EXPIRY,
            QueryStringConstants.SIGNED_RESOURCE,
            QueryStringConstants.SIGNED_IDENTIFIER,
            QueryStringConstants.SIGNED_IP,
            QueryStringConstants.SIGNED_PROTOCOL,
            QueryStringConstants.SIGNED_VERSION,
            QueryStringConstants.SIGNED_CACHE_CONTROL,
            QueryStringConstants.SIGNED_CONTENT_DISPOSITION,
            QueryStringConstants.SIGNED_CONTENT_ENCODING,
            QueryStringConstants.SIGNED_CONTENT_LANGUAGE,
            QueryStringConstants.SIGNED_CONTENT_TYPE,
            QueryStringConstants.START_PK,
            QueryStringConstants.START_RK,
            QueryStringConstants.END_PK,
            QueryStringConstants.END_RK,
            QueryStringConstants.SIGNED_RESOURCE_TYPES,
            QueryStringConstants.SIGNED_SERVICES,
            QueryStringConstants.SIGNED_OID,
            QueryStringConstants.SIGNED_TID,
            QueryStringConstants.SIGNED_KEY_START,
            QueryStringConstants.SIGNED_KEY_EXPIRY,
            QueryStringConstants.SIGNED_KEY_SERVICE,
            QueryStringConstants.SIGNED_KEY_VERSION,
            QueryStringConstants.SIGNED_ENCRYPTION_SCOPE,
            QueryStringConstants.SIGNED_KEY_DELEGATED_USER_TID,
            QueryStringConstants.SIGNED_DELEGATED_USER_OID,
            # for ADLS
            QueryStringConstants.SIGNED_AUTHORIZED_OID,
            QueryStringConstants.SIGNED_UNAUTHORIZED_OID,
            QueryStringConstants.SIGNED_CORRELATION_ID,
            QueryStringConstants.SIGNED_DIRECTORY_DEPTH,
        ]


class SharedAccessSignature(object):
    """
    Provides a factory for creating account access
    signature tokens with an account name and account key. Users can either
    use the factory or can construct the appropriate service and use the
    generate_*_shared_access_signature method directly.
    """

    def __init__(self, account_name, account_key, x_ms_version=X_MS_VERSION):
        """
        :param str account_name:
            The storage account name used to generate the shared access signatures.
        :param str account_key:
            The access key to generate the shares access signatures.
        :param str x_ms_version:
            The service version used to generate the shared access signatures.
        """
        self.account_name = account_name
        self.account_key = account_key
        self.x_ms_version = x_ms_version

    def generate_account(
        self,
        services,
        resource_types,
        permission,
        expiry,
        start=None,
        ip=None,
        protocol=None,
        sts_hook=None,
    ) -> str:
        """
        Generates a shared access signature for the account.
        Use the returned signature with the sas_token parameter of the service
        or to create a new account object.

        :param Any services: The specified services associated with the shared access signature.
        :param ResourceTypes resource_types:
            Specifies the resource types that are accessible with the account
            SAS. You can combine values to provide access to more than one
            resource type.
        :param AccountSasPermissions permission:
            The permissions associated with the shared access signature. The
            user is restricted to operations allowed by the permissions.
            Required unless an id is given referencing a stored access policy
            which contains this field. This field must be omitted if it has been
            specified in an associated stored access policy. You can combine
            values to provide more than one permission.
        :param expiry:
            The time at which the shared access signature becomes invalid.
            Required unless an id is given referencing a stored access policy
            which contains this field. This field must be omitted if it has
            been specified in an associated stored access policy. Azure will always
            convert values to UTC. If a date is passed in without timezone info, it
            is assumed to be UTC.
        :type expiry: datetime or str
        :param start:
            The time at which the shared access signature becomes valid. If
            omitted, start time for this call is assumed to be the time when the
            storage service receives the request. The provided datetime will always
            be interpreted as UTC.
        :type start: datetime or str
        :param str ip:
            Specifies an IP address or a range of IP addresses from which to accept requests.
            If the IP address from which the request originates does not match the IP address
            or address range specified on the SAS token, the request is not authenticated.
            For example, specifying sip=168.1.5.65 or sip=168.1.5.60-168.1.5.70 on the SAS
            restricts the request to those IP addresses.
        :param str protocol:
            Specifies the protocol permitted for a request made. The default value
            is https,http. See :class:`~azure.storage.common.models.Protocol` for possible values.
        :param sts_hook:
            For debugging purposes only. If provided, the hook is called with the string to sign
            that was used to generate the SAS.
        :type sts_hook: Optional[Callable[[str], None]]
        :returns: The generated SAS token for the account.
        :rtype: str
        """
        sas = _SharedAccessHelper()
        sas.add_base(permission, expiry, start, ip, protocol, self.x_ms_version)
        sas.add_account(services, resource_types)
        sas.add_account_signature(self.account_name, self.account_key)

        if sts_hook is not None:
            sts_hook(sas.string_to_sign)

        return sas.get_token()


class _SharedAccessHelper(object):
    def __init__(self):
        self.query_dict = {}
        self.string_to_sign = ""

    def _add_query(self, name, val):
        if val:
            self.query_dict[name] = str(val) if val is not None else None

    def add_base(self, permission, expiry, start, ip, protocol, x_ms_version):
        if isinstance(start, date):
            start = _to_utc_datetime(start)

        if isinstance(expiry, date):
            expiry = _to_utc_datetime(expiry)

        self._add_query(QueryStringConstants.SIGNED_START, start)
        self._add_query(QueryStringConstants.SIGNED_EXPIRY, expiry)
        self._add_query(QueryStringConstants.SIGNED_PERMISSION, permission)
        self._add_query(QueryStringConstants.SIGNED_IP, ip)
        self._add_query(QueryStringConstants.SIGNED_PROTOCOL, protocol)
        self._add_query(QueryStringConstants.SIGNED_VERSION, x_ms_version)

    def add_resource(self, resource):
        self._add_query(QueryStringConstants.SIGNED_RESOURCE, resource)

    def add_id(self, policy_id):
        self._add_query(QueryStringConstants.SIGNED_IDENTIFIER, policy_id)

    def add_account(self, services, resource_types):
        self._add_query(QueryStringConstants.SIGNED_SERVICES, services)
        self._add_query(QueryStringConstants.SIGNED_RESOURCE_TYPES, resource_types)

    def add_override_response_headers(
        self, cache_control, content_disposition, content_encoding, content_language, content_type
    ):
        self._add_query(QueryStringConstants.SIGNED_CACHE_CONTROL, cache_control)
        self._add_query(QueryStringConstants.SIGNED_CONTENT_DISPOSITION, content_disposition)
        self._add_query(QueryStringConstants.SIGNED_CONTENT_ENCODING, content_encoding)
        self._add_query(QueryStringConstants.SIGNED_CONTENT_LANGUAGE, content_language)
        self._add_query(QueryStringConstants.SIGNED_CONTENT_TYPE, content_type)

    def add_account_signature(self, account_name, account_key):
        def get_value_to_append(query):
            return_value = self.query_dict.get(query) or ""
            return return_value + "\n"

        string_to_sign = (
            account_name
            + "\n"
            + get_value_to_append(QueryStringConstants.SIGNED_PERMISSION)
            + get_value_to_append(QueryStringConstants.SIGNED_SERVICES)
            + get_value_to_append(QueryStringConstants.SIGNED_RESOURCE_TYPES)
            + get_value_to_append(QueryStringConstants.SIGNED_START)
            + get_value_to_append(QueryStringConstants.SIGNED_EXPIRY)
            + get_value_to_append(QueryStringConstants.SIGNED_IP)
            + get_value_to_append(QueryStringConstants.SIGNED_PROTOCOL)
            + get_value_to_append(QueryStringConstants.SIGNED_VERSION)
            + "\n"  # Signed Encryption Scope - always empty for queue
        )

        self._add_query(QueryStringConstants.SIGNED_SIGNATURE, sign_string(account_key, string_to_sign))
        self.string_to_sign = string_to_sign

    def get_token(self) -> str:
        return "&".join([f"{n}={url_quote(v)}" for n, v in self.query_dict.items() if v is not None])
