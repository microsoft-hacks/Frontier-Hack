"""Run classifier -> delimited findings -> advisor with a correlated function-call loop."""

import os
import sys
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "challenge-1-build"))
from agents import ADVISOR_NAME, CLASSIFIER_NAME, run_with_tool  # noqa: E402


def run_without_tools(client: AIProjectClient, agent_name: str, prompt: str) -> str:
    openai_client = client.get_openai_client()
    conversation = openai_client.conversations.create()
    try:
        response = openai_client.responses.create(
            input=prompt,
            conversation=conversation.id,
            extra_body={"agent_reference": {"name": agent_name, "type": "agent_reference"}},
        )
        return response.output_text
    finally:
        openai_client.conversations.delete(conversation_id=conversation.id)


def main() -> None:
    repository_root = Path(__file__).resolve().parents[3]
    load_dotenv(repository_root / ".env")
    endpoint = os.getenv("PROJECT_CONNECTION_STRING")
    if not endpoint:
        sys.exit("PROJECT_CONNECTION_STRING is not set. Complete Challenge 0 first.")

    client = AIProjectClient(endpoint=endpoint, credential=DefaultAzureCredential())
    try:
        existing_names = {agent.name for agent in client.agents.list()}
        missing = [name for name in (CLASSIFIER_NAME, ADVISOR_NAME) if name not in existing_names]
        if missing:
            sys.exit("Challenge 1 is required. Missing agents: " + ", ".join(missing))

        requested_assets = ", ".join(f"DRIVE-{number}" for number in range(101, 106))
        print("Stage 1: classifier with get_asset_condition")
        findings = run_with_tool(client, CLASSIFIER_NAME, f"Classify {requested_assets}.")
        print(findings)
        advisor_prompt = (
            "Use only the delimited classifier findings below. Provide actions, urgency, and escalation.\n"
            "<classifier_findings>\n"
            f"{findings}\n"
            "</classifier_findings>"
        )
        print("\nStage 2: advisor receives delimited classifier findings")
        advice = run_without_tools(client, ADVISOR_NAME, advisor_prompt)
        print(advice)
    finally:
        client.close()


if __name__ == "__main__":
    main()