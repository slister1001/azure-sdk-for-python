# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
import pytest
from azure.mgmt.containerregistry.v2025_04_01 import ContainerRegistryManagementClient

from devtools_testutils import AzureMgmtRecordedTestCase, RandomNameResourceGroupPreparer, recorded_by_proxy

AZURE_LOCATION = "eastus"


@pytest.mark.skip("you may need to update the auto-generated test case before run it")
class TestContainerRegistryManagementReplicationsOperations(AzureMgmtRecordedTestCase):
    def setup_method(self, method):
        self.client = self.create_mgmt_client(ContainerRegistryManagementClient)

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_replications_list(self, resource_group):
        response = self.client.replications.list(
            resource_group_name=resource_group.name,
            registry_name="str",
            api_version="2025-04-01",
        )
        result = [r for r in response]
        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_replications_get(self, resource_group):
        response = self.client.replications.get(
            resource_group_name=resource_group.name,
            registry_name="str",
            replication_name="str",
            api_version="2025-04-01",
        )

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_replications_begin_create(self, resource_group):
        response = self.client.replications.begin_create(
            resource_group_name=resource_group.name,
            registry_name="str",
            replication_name="str",
            replication={
                "location": "str",
                "id": "str",
                "name": "str",
                "provisioningState": "str",
                "regionEndpointEnabled": True,
                "status": {"displayStatus": "str", "message": "str", "timestamp": "2020-02-20 00:00:00"},
                "systemData": {
                    "createdAt": "2020-02-20 00:00:00",
                    "createdBy": "str",
                    "createdByType": "str",
                    "lastModifiedAt": "2020-02-20 00:00:00",
                    "lastModifiedBy": "str",
                    "lastModifiedByType": "str",
                },
                "tags": {"str": "str"},
                "type": "str",
                "zoneRedundancy": "str",
            },
            api_version="2025-04-01",
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_replications_begin_delete(self, resource_group):
        response = self.client.replications.begin_delete(
            resource_group_name=resource_group.name,
            registry_name="str",
            replication_name="str",
            api_version="2025-04-01",
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_replications_begin_update(self, resource_group):
        response = self.client.replications.begin_update(
            resource_group_name=resource_group.name,
            registry_name="str",
            replication_name="str",
            replication_update_parameters={"regionEndpointEnabled": bool, "tags": {"str": "str"}},
            api_version="2025-04-01",
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...
