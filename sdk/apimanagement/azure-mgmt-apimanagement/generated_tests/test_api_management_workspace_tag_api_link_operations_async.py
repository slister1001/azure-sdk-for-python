# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
import pytest
from azure.mgmt.apimanagement.aio import ApiManagementClient

from devtools_testutils import AzureMgmtRecordedTestCase, RandomNameResourceGroupPreparer
from devtools_testutils.aio import recorded_by_proxy_async

AZURE_LOCATION = "eastus"


@pytest.mark.skip("you may need to update the auto-generated test case before run it")
class TestApiManagementWorkspaceTagApiLinkOperationsAsync(AzureMgmtRecordedTestCase):
    def setup_method(self, method):
        self.client = self.create_mgmt_client(ApiManagementClient, is_async=True)

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy_async
    async def test_workspace_tag_api_link_list_by_product(self, resource_group):
        response = self.client.workspace_tag_api_link.list_by_product(
            resource_group_name=resource_group.name,
            service_name="str",
            workspace_id="str",
            tag_id="str",
            api_version="2024-05-01",
        )
        result = [r async for r in response]
        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy_async
    async def test_workspace_tag_api_link_get(self, resource_group):
        response = await self.client.workspace_tag_api_link.get(
            resource_group_name=resource_group.name,
            service_name="str",
            workspace_id="str",
            tag_id="str",
            api_link_id="str",
            api_version="2024-05-01",
        )

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy_async
    async def test_workspace_tag_api_link_create_or_update(self, resource_group):
        response = await self.client.workspace_tag_api_link.create_or_update(
            resource_group_name=resource_group.name,
            service_name="str",
            workspace_id="str",
            tag_id="str",
            api_link_id="str",
            parameters={"apiId": "str", "id": "str", "name": "str", "type": "str"},
            api_version="2024-05-01",
        )

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy_async
    async def test_workspace_tag_api_link_delete(self, resource_group):
        response = await self.client.workspace_tag_api_link.delete(
            resource_group_name=resource_group.name,
            service_name="str",
            workspace_id="str",
            tag_id="str",
            api_link_id="str",
            api_version="2024-05-01",
        )

        # please add some check logic here by yourself
        # ...
