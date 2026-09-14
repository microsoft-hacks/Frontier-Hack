"""Run classifier -> delimited findings -> advisor with a correlated function-call loop."""

import os
import sys
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "challenge-1-build"))
from agents import ADVISOR_NAME, CLASSIFIER_NAME, run_agent, run_with_tool  # noqa: E402


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

        requested_assets = ", ".join(["MOTOR-201", "GEN-301", "XFR-401", "DRIVE-101", "VFD-501"])
        print("Stage 1: classifier with get_asset_condition")
        findings = run_with_tool(client, CLASSIFIER_NAME, f"Classifique {requested_assets}.")
        print(findings)
        advisor_prompt = (
            "Use os achados do classificador delimitados abaixo e a base de conhecimento "
            "(Azure AI Search). Forneça ações, urgência e escalonamento e cite a fonte de cada ação.\n"
            "<classifier_findings>\n"
            f"{findings}\n"
            "</classifier_findings>"
        )
        print("\nStage 2: advisor anchors recommendations on classifier findings and the knowledge base")
        advice = run_agent(client, ADVISOR_NAME, advisor_prompt)
        print(advice)
    finally:
        client.close()


if __name__ == "__main__":
    main()