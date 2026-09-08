"""Run the persistent classifier with tracing enabled."""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(REPOSITORY_ROOT / ".env")


def configure_tracing() -> None:
    from azure.ai.projects.telemetry import AIProjectInstrumentor
    from azure.monitor.opentelemetry import configure_azure_monitor

    AIProjectInstrumentor().instrument()
    configure_azure_monitor(
        connection_string=os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"),
        enable_live_metrics=True,
    )


def main() -> None:
    endpoint = os.getenv("PROJECT_CONNECTION_STRING")
    if not endpoint or os.getenv("AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING") != "true":
        sys.exit("Tracing environment variables are missing. Complete Challenge 0 first.")

    configure_tracing()
    from azure.ai.projects import AIProjectClient
    from azure.identity import DefaultAzureCredential

    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "challenge-1-build"))
    from agents import CLASSIFIER_NAME, run_with_tool

    client = AIProjectClient(endpoint=endpoint, credential=DefaultAzureCredential())
    try:
        existing_names = {agent.name for agent in client.agents.list()}
        if CLASSIFIER_NAME not in existing_names:
            sys.exit(f"Challenge 1 is required. Missing agent: {CLASSIFIER_NAME}")
        print(
            run_with_tool(
                client,
                CLASSIFIER_NAME,
                "Call get_asset_condition for DRIVE-103 and classify it with evidence.",
            )
        )
    finally:
        client.close()


if __name__ == "__main__":
    main()