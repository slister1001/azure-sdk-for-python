# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
import time
from functools import partial

import pytest
from azure.core.exceptions import ResourceExistsError
from azure.keyvault.administration import KeyVaultBackupClient
from azure.keyvault.administration._internal import parse_folder_url
from azure.keyvault.administration._internal.client_base import DEFAULT_VERSION
from devtools_testutils import recorded_by_proxy, set_bodiless_matcher

from _shared.test_case import KeyVaultTestCase
from _test_case import KeyVaultBackupClientPreparer, KeyVaultBackupClientSasPreparer, get_decorator

all_api_versions = get_decorator()
only_default = get_decorator(api_versions=[DEFAULT_VERSION])


class TestBackupClientTests(KeyVaultTestCase):

    def create_key_client(self, vault_uri, **kwargs):
        from azure.keyvault.keys import KeyClient
        credential = self.get_credential(KeyClient)
        return self.create_client_from_credential(KeyClient, credential=credential, vault_url=vault_uri, **kwargs )

    @pytest.mark.parametrize("api_version", only_default)
    @KeyVaultBackupClientPreparer()
    @recorded_by_proxy
    def test_full_backup_and_restore(self, client, **kwargs):
        set_bodiless_matcher()
        # backup the vault
        container_uri = kwargs.pop("container_uri")
        # make sure an error isn't raised by pre-backup check; i.e. ensure the backup can be done
        client.begin_pre_backup(container_uri, use_managed_identity=True).wait()
        backup_poller = client.begin_backup(container_uri, use_managed_identity=True)
        backup_operation = backup_poller.result()
        assert backup_operation.folder_url

        if self.is_live:
            # Additional waiting to ensure backup will be available for restore. Otherwise, can get the following:
            # "This Managed HSM hasn't been backed up within the safe time limit of 30 minutes"
            time.sleep(15)

        # restore the backup
        # make sure an error isn't raised by pre-restore check; i.e. ensure the restore can be done
        client.begin_pre_restore(backup_operation.folder_url, use_managed_identity=True).wait()
        restore_poller = client.begin_restore(backup_operation.folder_url, use_managed_identity=True)
        restore_poller.wait()
        if self.is_live:
            time.sleep(60)  # additional waiting to avoid conflicts with resources in other tests

    @pytest.mark.parametrize("api_version", only_default)
    @KeyVaultBackupClientPreparer()
    @recorded_by_proxy
    def test_full_backup_and_restore_rehydration(self, client, **kwargs):
        set_bodiless_matcher()
        container_uri = kwargs.pop("container_uri")

        # backup the vault
        backup_poller = client.begin_backup(blob_storage_url=container_uri, use_managed_identity=True)

        # create a new poller from a continuation token
        token = backup_poller.continuation_token()
        rehydrated = client.begin_backup(container_uri, use_managed_identity=True, continuation_token=token)

        rehydrated_operation = rehydrated.result()
        assert rehydrated_operation.folder_url
        backup_operation = backup_poller.result()
        assert backup_operation.folder_url == rehydrated_operation.folder_url

        if self.is_live:
            time.sleep(15)  # Additional waiting to ensure backup will be available for restore

        # restore the backup
        restore_poller = client.begin_restore(folder_url=backup_operation.folder_url, use_managed_identity=True)

        # create a new poller from a continuation token
        token = restore_poller.continuation_token()
        rehydrated = client.begin_restore(
            backup_operation.folder_url, use_managed_identity=True, continuation_token=token
        )

        rehydrated.wait()
        restore_poller.wait()
        if self.is_live:
            time.sleep(60)  # additional waiting to avoid conflicts with resources in other tests

    @pytest.mark.parametrize("api_version", only_default)
    @KeyVaultBackupClientPreparer()
    @recorded_by_proxy
    def test_selective_key_restore(self, client, **kwargs):
        set_bodiless_matcher()
        # create a key to selectively restore
        managed_hsm_url = kwargs.pop("managed_hsm_url")
        key_client = self.create_key_client(managed_hsm_url)
        key_name = self.get_resource_name("selective-restore-test-key")
        key_client.create_rsa_key(key_name)


        # backup the vault
        container_uri = kwargs.pop("container_uri")
        backup_poller = client.begin_backup(container_uri, use_managed_identity=True)
        backup_operation = backup_poller.result()

        if self.is_live:
            time.sleep(15)  # Additional waiting to ensure backup will be available for restore

        # restore the key
        restore_poller = client.begin_restore(backup_operation.folder_url, use_managed_identity=True, key_name=key_name)
        restore_poller.wait()

        # delete the key
        delete_function = partial(key_client.begin_delete_key, key_name)
        delete_poller = self._poll_until_no_exception(delete_function, ResourceExistsError)
        delete_poller.wait()
        key_client.purge_deleted_key(key_name)
        if self.is_live:
            time.sleep(60)  # additional waiting to avoid conflicts with resources in other tests

    @pytest.mark.parametrize("api_version", only_default)
    @KeyVaultBackupClientPreparer()
    @recorded_by_proxy
    def test_backup_client_polling(self, client, **kwargs):
        set_bodiless_matcher()

        # backup the vault
        container_uri = kwargs.pop("container_uri")
        backup_poller = client.begin_backup(container_uri, use_managed_identity=True)

        # create a new poller from a continuation token
        token = backup_poller.continuation_token()
        rehydrated = client.begin_backup(container_uri, use_managed_identity=True, continuation_token=token)

        # check that pollers and polling methods behave as expected
        if self.is_live:
            assert backup_poller.status() == "InProgress"
            assert not backup_poller.done() or backup_poller.polling_method().finished()
            assert rehydrated.status() == "InProgress"
            assert not rehydrated.done() or rehydrated.polling_method().finished()

        backup_operation = backup_poller.result()
        assert backup_poller.status() == "Succeeded" and backup_poller.polling_method().status() == "Succeeded"
        rehydrated_operation = rehydrated.result()
        assert rehydrated.status() == "Succeeded" and rehydrated.polling_method().status() == "Succeeded"
        assert backup_operation.folder_url == rehydrated_operation.folder_url

        # rehydrate a poller with a continuation token of a completed operation
        late_rehydrated = client.begin_backup(container_uri, use_managed_identity=True, continuation_token=token)
        assert late_rehydrated.status() == "Succeeded"
        late_rehydrated.wait()

        if self.is_live:
            time.sleep(15)  # Additional waiting to ensure backup will be available for restore

        # restore the backup
        restore_poller = client.begin_restore(backup_operation.folder_url, use_managed_identity=True)

        # create a new poller from a continuation token
        token = restore_poller.continuation_token()
        rehydrated = client.begin_restore(
            backup_operation.folder_url, use_managed_identity=True, continuation_token=token
        )

        # check that pollers and polling methods behave as expected
        if self.is_live:
            assert restore_poller.status() == "InProgress"
            assert not restore_poller.done() or restore_poller.polling_method().finished()
            assert rehydrated.status() == "InProgress"
            assert not rehydrated.done() or rehydrated.polling_method().finished()

        rehydrated.wait()
        assert rehydrated.status() == "Succeeded" and rehydrated.polling_method().status() == "Succeeded"
        restore_poller.wait()
        assert restore_poller.status() == "Succeeded" and restore_poller.polling_method().status() == "Succeeded"

        if self.is_live:
            time.sleep(60)  # additional waiting to avoid conflicts with resources in other tests

    @pytest.mark.live_test_only
    @pytest.mark.parametrize("api_version", only_default)
    @KeyVaultBackupClientSasPreparer()
    def test_backup_restore_sas(self, client: KeyVaultBackupClient, **kwargs):
        # backup the vault
        container_uri = kwargs.pop("container_uri")
        sas_token = kwargs.pop("sas_token")

        if self.is_live and not sas_token:
            pytest.skip("SAS token is required for live tests. Please set the BLOB_STORAGE_SAS_TOKEN environment variable.")

        client.begin_pre_backup(container_uri, sas_token=sas_token).wait()
        backup_poller = client.begin_backup(container_uri, sas_token)  # Test positional SAS token for backwards compat
        backup_operation = backup_poller.result()
        assert backup_operation.folder_url

        if self.is_live:
            time.sleep(15)  # Additional waiting to ensure backup will be available for restore

        # restore the backup
        client.begin_pre_restore(backup_operation.folder_url, sas_token=sas_token).wait()
        restore_poller = client.begin_restore(backup_operation.folder_url, sas_token)  # Test positional SAS token
        restore_poller.wait()
        if self.is_live:
            time.sleep(60)  # additional waiting to avoid conflicts with resources in other tests


@pytest.mark.parametrize(
    "url,expected_container_url,expected_folder_name",
    [
        (
            "https://account.blob.core.windows.net/backup/mhsm-account-2020090117323313",
            "https://account.blob.core.windows.net/backup",
            "mhsm-account-2020090117323313",
        ),
        ("https://account.storage/account/storage", "https://account.storage/account", "storage"),
        ("https://account.storage/a/b/c", "https://account.storage/a", "b/c"),
        ("https://account.storage/a/b-c", "https://account.storage/a", "b-c"),
    ],
)
def test_parse_folder_url(url, expected_container_url, expected_folder_name):
    container_url, folder_name = parse_folder_url(url)
    assert container_url == expected_container_url
    assert folder_name == expected_folder_name
