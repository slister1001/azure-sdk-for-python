from typing import Optional, Dict, Any
import os

# Azure imports
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from azure.ai.evaluation.red_team import RedTeam, RiskCategory, AttackStrategy
from azure.ai.projects import AIProjectClient
import azure.ai.agents
import time
# OpenAI imports
from openai import AzureOpenAI
from azure.ai.agents.models import ListSortOrder
async def run_red_team():
    # Initialize Azure credentials
    credential = DefaultAzureCredential()
    # endpoint = os.environ["PROJECT_ENDPOINT"]
    # model_deployment_name = os.environ["MODEL_DEPLOYMENT_NAME"]
    # agent_id = os.environ["AGENT_ID"]
    # proj = {
    # "subscription_id": "fac34303-435d-4486-8c3f-7094d82a0b60",
    # "resource_group_name": "rg-naarkalgaihub",
    # "project_name": "naarkalg-rai-test",
    # }
    endpoint = "https://np-wus2-resource.services.ai.azure.com/api/projects/np-wus2"
    model_deployment_name = "gpt-4o"
    agent_id = "asst_S82oUcyuwJFL1qX09dZlK7yA"
    with DefaultAzureCredential(exclude_interactive_browser_credential=False) as credential:
        with AIProjectClient(endpoint=endpoint, credential=credential) as project_client:
            # agent = project_client.agents.get_agent(agent_id)
            # thread = project_client.agents.threads.create()

            def agent_callback(query: str) -> str:
                message = project_client.agents.messages.create(thread_id=thread.id, role="user", content=query)
                run = project_client.agents.runs.create(thread_id=thread.id, agent_id=agent.id)

                # Poll the run as long as run status is queued or in progress
                while run.status in ["queued", "in_progress", "requires_action"]:
                    # Wait for a second
                    time.sleep(1)
                    run = project_client.agents.runs.get(thread_id=thread.id, run_id=run.id)
                    # [END create_run]
                    print(f"Run status: {run.status}")

                if run.status == "failed":
                    print(f"Run error: {run.last_error}")
                    return "Error: Agent run failed."
                messages = project_client.agents.messages.list(thread_id=thread.id, order=ListSortOrder.DESCENDING)
                for msg in messages:
                    if msg.text_messages:
                        return msg.text_messages[0].text.value
                return "Could not get a response from the agent."
        

            red_team = RedTeam(
                azure_ai_project=endpoint,
                credential=credential,
                num_objectives=1,
                output_dir="redteam_outputs/"
            )

            result = await red_team.scan(
                target=agent_callback,
                scan_name="Agent-Scan",
                attack_strategies=[AttackStrategy.Flip, AttackStrategy.Tense, AttackStrategy.Compose([
                    AttackStrategy.Base64,
                    AttackStrategy.Morse,
                ])],
                skip_upload=True,
            )

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_red_team())