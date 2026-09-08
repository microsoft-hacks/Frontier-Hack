"""Create and exercise the two persistent Electric Plant agents."""

import json
import os
import sys
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import FunctionTool, PromptAgentDefinition
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
from openai.types.responses.response_input_param import FunctionCallOutput


CLASSIFIER_NAME = "asset-health-classifier-agent"
ADVISOR_NAME = "maintenance-efficiency-advisor-agent"
API_PATH = Path(__file__).resolve().parents[1] / "api-data"
REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(API_PATH))
from data_store import get_asset_condition as read_asset_condition  # noqa: E402

load_dotenv(REPOSITORY_ROOT / ".env")
MODEL_DEPLOYMENT_NAME = os.getenv("MODEL_DEPLOYMENT_NAME", "gpt-5.4")

CLASSIFIER_INSTRUCTIONS = """## Purpose
Classify Northline Motion Works drive assets by comparing every reading with that asset's thresholds. Call get_asset_condition for every requested asset. Use these fallback thresholds only when tool data is unavailable: vibration 0-4.0 mm/s RMS; winding temperature 20-85 C; current load 25-90 percent rated; operating efficiency 90-100 percent.

## OutputFormat
Return only a Markdown table with Asset, Vibration, Winding temperature, Current load, Operating efficiency, Status, and Evidence columns. Use exactly: 🔴 critical, ⚠️ warning, ✅ normal. Show values, units, and violated thresholds as evidence.

## Scope
Classify DRIVE-101 through DRIVE-105 from supplied readings or tool results. Treat multiple simultaneous safety-sensitive violations, especially vibration plus winding temperature, as critical.

## Guardrails
Never recommend actions. Never invent readings or thresholds. Prefer entity-specific tool thresholds over fallbacks. If an asset is unknown or evidence is missing, state that in the table.
"""

ADVISOR_INSTRUCTIONS = """## Purpose
Turn a classifier's structured findings into maintenance actions, urgency, and escalation guidance for Northline Motion Works.

## OutputFormat
For each asset, return Status, Urgency, Evidence received, Recommended action, and Escalation. Use exactly: 🔴 critical, ⚠️ warning, ✅ normal.

## Scope
Use only classifier findings supplied in the request. For compound vibration and winding-temperature failures, require a controlled shutdown, isolation under site procedure, and immediate safety/maintenance escalation. For warnings, recommend inspection or planned maintenance. For normal assets, continue monitoring.

## Guardrails
Do not invent, alter, or reclassify readings or thresholds. Do not claim a shutdown occurred. Preserve uncertainty and direct personnel to approved site safety procedures.
"""


def _load_environment() -> str | None:
    return os.getenv("PROJECT_CONNECTION_STRING")


def get_asset_condition(asset_id: str) -> str:
    """Return readings and entity-specific thresholds for one known drive asset."""
    condition = read_asset_condition(asset_id)
    if condition is None:
        return json.dumps({"error": f"Asset '{asset_id}' was not found."})
    return json.dumps(condition)


ASSET_CONDITION_TOOL = FunctionTool(
    name="get_asset_condition",
    description=(
        "Get current readings, asset-specific thresholds, status, violations, and known issues "
        "for one drive. Always call it once per requested DRIVE-101 through DRIVE-105 asset."
    ),
    parameters={
        "type": "object",
        "properties": {
            "asset_id": {
                "type": "string",
                "description": "Asset ID, for example DRIVE-103",
            }
        },
        "required": ["asset_id"],
        "additionalProperties": False,
    },
    strict=True,
)


def run_with_tool(client: AIProjectClient, agent_name: str, prompt: str) -> str:
    openai_client = client.get_openai_client()
    conversation = openai_client.conversations.create()
    reference = {"agent_reference": {"name": agent_name, "type": "agent_reference"}}
    try:
        response = openai_client.responses.create(
            input=prompt, conversation=conversation.id, extra_body=reference
        )
        while True:
            calls = [item for item in response.output if item.type == "function_call"]
            if not calls:
                return response.output_text
            outputs = []
            for call in calls:
                arguments = json.loads(call.arguments)
                if call.name != "get_asset_condition":
                    raise RuntimeError(f"Unexpected tool call: {call.name}")
                outputs.append(
                    FunctionCallOutput(
                        type="function_call_output",
                        call_id=call.call_id,
                        output=get_asset_condition(arguments["asset_id"]),
                    )
                )
            response = openai_client.responses.create(
                input=outputs, conversation=conversation.id, extra_body=reference
            )
    finally:
        openai_client.conversations.delete(conversation_id=conversation.id)


def main() -> None:
    endpoint = _load_environment()
    if not endpoint:
        sys.exit("PROJECT_CONNECTION_STRING is not set. Complete Challenge 0 first.")
    client = AIProjectClient(endpoint=endpoint, credential=DefaultAzureCredential())
    try:
        classifier = client.agents.create_version(
            agent_name=CLASSIFIER_NAME,
            definition=PromptAgentDefinition(
                model=MODEL_DEPLOYMENT_NAME,
                instructions=CLASSIFIER_INSTRUCTIONS,
                tools=[ASSET_CONDITION_TOOL],
            ),
        )
        advisor = client.agents.create_version(
            agent_name=ADVISOR_NAME,
            definition=PromptAgentDefinition(
                model=MODEL_DEPLOYMENT_NAME,
                instructions=ADVISOR_INSTRUCTIONS,
            ),
        )
        print(f"Created {classifier.name} version {classifier.version} with get_asset_condition.")
        print(f"Created {advisor.name} version {advisor.version} with no tools.")
        print(run_with_tool(client, classifier.name, "Classify DRIVE-103 using the data tool."))
    finally:
        client.close()


if __name__ == "__main__":
    main()