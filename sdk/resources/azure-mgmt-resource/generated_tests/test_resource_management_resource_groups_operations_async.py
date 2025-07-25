# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
import pytest
from azure.mgmt.resource.resources.aio import ResourceManagementClient

from devtools_testutils import AzureMgmtRecordedTestCase, RandomNameResourceGroupPreparer
from devtools_testutils.aio import recorded_by_proxy_async

AZURE_LOCATION = "eastus"


@pytest.mark.skip("you may need to update the auto-generated test case before run it")
class TestResourceManagementResourceGroupsOperationsAsync(AzureMgmtRecordedTestCase):
    def setup_method(self, method):
        self.client = self.create_mgmt_client(ResourceManagementClient, is_async=True)

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy_async
    async def test_resource_groups_check_existence(self, resource_group):
        response = await self.client.resource_groups.check_existence(
            resource_group_name=resource_group.name,
            api_version="2025-04-01",
        )

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy_async
    async def test_resource_groups_create_or_update(self, resource_group):
        response = await self.client.resource_groups.create_or_update(
            resource_group_name=resource_group.name,
            parameters={
                "location": "str",
                "id": "str",
                "managedBy": "str",
                "name": "str",
                "properties": {"provisioningState": "str"},
                "tags": {"str": "str"},
                "type": "str",
            },
            api_version="2025-04-01",
        )

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy_async
    async def test_resource_groups_begin_delete(self, resource_group):
        response = await (
            await self.client.resource_groups.begin_delete(
                resource_group_name=resource_group.name,
                api_version="2025-04-01",
            )
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy_async
    async def test_resource_groups_get(self, resource_group):
        response = await self.client.resource_groups.get(
            resource_group_name=resource_group.name,
            api_version="2025-04-01",
        )

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy_async
    async def test_resource_groups_update(self, resource_group):
        response = await self.client.resource_groups.update(
            resource_group_name=resource_group.name,
            parameters={
                "managedBy": "str",
                "name": "str",
                "properties": {"provisioningState": "str"},
                "tags": {"str": "str"},
            },
            api_version="2025-04-01",
        )

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy_async
    async def test_resource_groups_begin_export_template(self, resource_group):
        response = await (
            await self.client.resource_groups.begin_export_template(
                resource_group_name=resource_group.name,
                parameters={"options": "str", "outputFormat": "str", "resources": ["str"]},
                api_version="2025-04-01",
            )
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy_async
    async def test_resource_groups_list(self, resource_group):
        response = self.client.resource_groups.list(
            api_version="2025-04-01",
        )
        result = [r async for r in response]
        # please add some check logic here by yourself
        # ...
