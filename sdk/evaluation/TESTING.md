# Testing Azure AI Evaluation

This document describes how to set up and run tests for the Azure AI Evaluation SDK.

## Prerequisites

- Python 3.9 or later
- [Azure subscription](https://azure.microsoft.com/free/)
- [PowerShell](https://docs.microsoft.com/powershell/scripting/install/installing-powershell) 7.0 or newer
- [Azure PowerShell](https://docs.microsoft.com/powershell/azure/install-az-ps) module

## Running Tests Locally

### Option 1: Using connections.json (Development)

For local development, you can create a `connections.json` file at `sdk/evaluation/azure-ai-evaluation/connections.json`:

```json
{
    "azure_ai_project_scope": {
        "value": {
            "subscription_id": "your-subscription-id",
            "resource_group_name": "your-resource-group",
            "project_name": "your-workspace-name"
        }
    },
    "azure_openai_model_config": {
        "value": {
            "azure_endpoint": "https://your-openai.openai.azure.com/",
            "api_version": "2023-07-01-preview",
            "azure_deployment": "gpt-35-turbo",
            "api_key": "your-api-key"
        }
    }
}
```

**Note:** Add `connections.json` to `.gitignore` to avoid committing secrets.

### Option 2: Using Test Resources (Recommended)

For a proper test environment, use the Azure SDK test resource provisioning:

1. Log in to Azure:
   ```powershell
   Connect-AzAccount -Subscription 'YOUR SUBSCRIPTION ID'
   ```

2. Provision test resources:
   ```powershell
   eng/common/TestResources/New-TestResources.ps1 evaluation
   ```

3. The script will output environment variables. Set them in your terminal:
   ```powershell
   # PowerShell example
   ${env:AZURE_AI_PROJECT_SUBSCRIPTION_ID} = '...'
   ${env:AZURE_AI_PROJECT_RESOURCE_GROUP_NAME} = '...'
   ${env:AZURE_AI_PROJECT_NAME} = '...'
   ${env:AZURE_OPENAI_ENDPOINT} = '...'
   ${env:AZURE_OPENAI_API_VERSION} = '...'
   ${env:AZURE_OPENAI_DEPLOYMENT_NAME} = '...'
   ${env:AZURE_OPENAI_KEY} = '...'
   ```

4. Run tests:
   ```bash
   cd sdk/evaluation/azure-ai-evaluation
   pytest
   ```

### Clean Up Test Resources

To remove test resources after testing:

```powershell
eng/common/TestResources/Remove-TestResources.ps1 evaluation
```

## CI/CD Testing

The weekly live test pipeline automatically:
1. Provisions resources using `test-resources.json` ARM template
2. Sets environment variables from template outputs
3. Runs live tests with provisioned resources
4. Cleans up resources after tests complete

## Test Modes

- **Live**: Tests run against real Azure resources (default for local testing)
- **Playback**: Tests use recorded responses (default for PR validation)
- **Record**: Tests run live and record responses for playback

## Resources Provisioned

The `test-resources.json` ARM template creates:

- **Azure Machine Learning Workspace**: Acts as the Azure AI project
- **Azure OpenAI Service**: Provides AI model deployments
  - gpt-35-turbo deployment
- **Storage Account**: Required by ML workspace
- **Key Vault**: Required by ML workspace for secrets
- **Application Insights**: Required by ML workspace for monitoring

## Troubleshooting

### "Connection not found in dev connections" Error

This error occurs when running live tests without proper configuration. Either:
1. Create a `connections.json` file (Option 1 above)
2. Provision test resources and set environment variables (Option 2 above)

### Azure OpenAI Quota Issues

If deployment fails due to quota, you can:
1. Request quota increase in Azure portal
2. Use a different region with available quota
3. Use an existing Azure OpenAI resource

### Region Availability

Azure OpenAI is not available in all regions. Recommended regions:
- East US
- South Central US
- West Europe

## Additional Resources

- [Azure SDK Python Testing Guide](https://github.com/Azure/azure-sdk-for-python/blob/main/doc/dev/tests.md)
- [Test Resource Management](../../eng/common/TestResources/README.md)
- [Azure AI Evaluation Documentation](https://aka.ms/azsdk/python/ai/evaluation)
