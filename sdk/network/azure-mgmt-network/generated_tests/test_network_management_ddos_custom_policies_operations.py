# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
import pytest
from azure.mgmt.network import NetworkManagementClient

from devtools_testutils import AzureMgmtRecordedTestCase, RandomNameResourceGroupPreparer, recorded_by_proxy

AZURE_LOCATION = "eastus"


@pytest.mark.skip("you may need to update the auto-generated test case before run it")
class TestNetworkManagementDdosCustomPoliciesOperations(AzureMgmtRecordedTestCase):
    def setup_method(self, method):
        self.client = self.create_mgmt_client(NetworkManagementClient)

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_ddos_custom_policies_begin_delete(self, resource_group):
        response = self.client.ddos_custom_policies.begin_delete(
            resource_group_name=resource_group.name,
            ddos_custom_policy_name="str",
            api_version="2024-07-01",
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_ddos_custom_policies_get(self, resource_group):
        response = self.client.ddos_custom_policies.get(
            resource_group_name=resource_group.name,
            ddos_custom_policy_name="str",
            api_version="2024-07-01",
        )

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_ddos_custom_policies_begin_create_or_update(self, resource_group):
        response = self.client.ddos_custom_policies.begin_create_or_update(
            resource_group_name=resource_group.name,
            ddos_custom_policy_name="str",
            parameters={
                "etag": "str",
                "id": "str",
                "location": "str",
                "name": "str",
                "provisioningState": "str",
                "resourceGuid": "str",
                "tags": {"str": "str"},
                "type": "str",
            },
            api_version="2024-07-01",
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_ddos_custom_policies_update_tags(self, resource_group):
        response = self.client.ddos_custom_policies.update_tags(
            resource_group_name=resource_group.name,
            ddos_custom_policy_name="str",
            parameters={"tags": {"str": "str"}},
            api_version="2024-07-01",
        )

        # please add some check logic here by yourself
        # ...
