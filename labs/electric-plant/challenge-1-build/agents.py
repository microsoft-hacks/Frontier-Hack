"""Create and exercise the two persistent Electric Plant agents."""

import json
import os
import sys
from pathlib import Path
from typing import Callable

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    AISearchIndexResource,
    AzureAISearchQueryType,
    AzureAISearchTool,
    AzureAISearchToolResource,
    FunctionTool,
    PromptAgentDefinition,
)
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
from openai.types.responses.response_input_param import FunctionCallOutput


CLASSIFIER_NAME = "electric-plant-1-classifier-agent"
ADVISOR_NAME = "maintenance-efficiency-advisor-agent"
SEARCH_CONNECTION_NAME = "search-hack-shared"
SEARCH_INDEX_NAME = "electric-plant-maintenance"
API_PATH = Path(__file__).resolve().parents[1] / "api-data"
REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(API_PATH))
from data_store import get_asset_condition as read_asset_condition  # noqa: E402

load_dotenv(REPOSITORY_ROOT / ".env")
MODEL_DEPLOYMENT_NAME = os.getenv("MODEL_DEPLOYMENT_NAME", "gpt-5.4")

CLASSIFIER_INSTRUCTIONS = """
## Propósito
-  Você é um assistente de IA para a Smart Electric, referência global em motores, geradores, transformadores e controles elétricos com oferta integrada para eletrificação, automação e digitalização, que ajuda o usuário a classificar as condições dos ativos.

## Contexto
Tente carregar os dados por meio das ferramentas ou use os limites padrão =
- vibração: 0-4,0 mm/s RMS
- temperatura do enrolamento: 20-85 °C
- carga de corrente: 25-90 %
- eficiência operacional: 90-100 %.

## Formato de Saída
- SOMENTE a tabela de resumo da classificação
- linhas = para cada ativo.
- colunas = para cada métrica
- use 🔴 para crítico, ⚠️ para alto, e ✅ para baixo.
- adicione uma coluna de prioridade com base na classificação das métricas

## Escopo
- Antes de responder, verifique se a solicitação está relacionada a este Propósito.
- Se estiver no escopo: continue a conversa.
- Se estiver fora do escopo: não responda ao conteúdo da solicitação. Apenas explique o seu propósito

## Guardrails
- Não crie dados de clientes.
- Não recomende nada
- Se faltarem dados-chave, faça perguntas de acompanhamento precisas.
"""

ADVISOR_INSTRUCTIONS = """## Propósito
Transformar os achados estruturados de um classificador em ações de manutenção, urgência e orientações de escalonamento para a Smart Electric, ancoradas na base de conhecimento técnico da empresa.

## Formato de Saída
Para cada ativo, retorne Status, Urgência, Evidências recebidas, Ação recomendada e Escalonamento. Use exatamente: 🔴 crítico, ⚠️ aviso, ✅ normal. Cite o documento da base de conhecimento usado como fonte de cada Ação recomendada (ex.: [cbm], [vibracao], [transformador-potencia]).

## Escopo
Consulte a base de conhecimento via Azure AI Search para fundamentar a técnica e o procedimento de cada recomendação, além dos achados do classificador fornecidos na solicitação. Para falhas combinadas de vibração e temperatura do enrolamento, exija desligamento controlado, isolamento conforme o procedimento do local e escalonamento imediato de segurança/manutenção. Para avisos, recomende inspeção ou manutenção planejada. Para ativos normais, continue o monitoramento.

## Guardrails
Não invente leituras, limites ou procedimentos: somente utilize os achados recebidos e as diretrizes recuperadas da base. Cite a fonte de cada ação recomendada. Não afirme que um desligamento ocorreu. Preserve a incerteza e direcione o pessoal aos procedimentos de segurança aprovados no local.
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
        "Obtenha leituras atuais, limites específicos do ativo, status, violações e problemas "
        "conhecidos para um ativo. Sempre chame uma vez para cada ativo solicitado "
        "(MOTOR-201, GEN-301, XFR-401, DRIVE-101, VFD-501)."
    ),
    parameters={
        "type": "object",
        "properties": {
            "asset_id": {
                "type": "string",
                "description": "ID do ativo, por exemplo XFR-401",
            }
        },
        "required": ["asset_id"],
        "additionalProperties": False,
    },
    strict=True,
)


def build_search_tool(client: AIProjectClient) -> AzureAISearchTool:
    """Build the Azure AI Search tool over the shared maintenance knowledge index."""
    try:
        connection = client.connections.get(connection_name=SEARCH_CONNECTION_NAME)
    except Exception:
        from azure.ai.projects.models import ConnectionType

        connection = client.connections.get_default(ConnectionType.AZURE_AI_SEARCH)
    return AzureAISearchTool(
        azure_ai_search=AzureAISearchToolResource(
            indexes=[
                AISearchIndexResource(
                    project_connection_id=connection.id,
                    index_name=SEARCH_INDEX_NAME,
                    query_type=AzureAISearchQueryType.SIMPLE,
                )
            ]
        )
    )


def run_agent(
    client: AIProjectClient,
    agent_name: str,
    prompt: str,
    function_handlers: dict[str, Callable[..., str]] | None = None,
) -> str:
    """Run one agent turn, resolving any client-side function calls in a loop.

    Server-side tools (for example Azure AI Search) are resolved by the agent
    service; only ``function_call`` items are executed here.
    """
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
            handlers = function_handlers or {}
            for call in calls:
                if call.name not in handlers:
                    raise RuntimeError(f"Unexpected tool call: {call.name}")
                arguments = json.loads(call.arguments) if call.arguments else {}
                outputs.append(
                    FunctionCallOutput(
                        type="function_call_output",
                        call_id=call.call_id,
                        output=handlers[call.name](**arguments),
                    )
                )
            response = openai_client.responses.create(
                input=outputs, conversation=conversation.id, extra_body=reference
            )
    finally:
        openai_client.conversations.delete(conversation_id=conversation.id)


def run_with_tool(client: AIProjectClient, agent_name: str, prompt: str) -> str:
    """Run the classifier, resolving its get_asset_condition function tool."""
    return run_agent(client, agent_name, prompt, {"get_asset_condition": get_asset_condition})


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
                tools=[build_search_tool(client)],
            ),
        )
        print(f"Created {classifier.name} version {classifier.version} with get_asset_condition.")
        print(
            f"Created {advisor.name} version {advisor.version} with Azure AI Search "
            f"over index {SEARCH_INDEX_NAME}."
        )
        print(run_with_tool(client, classifier.name, "Classifique XFR-401 usando a ferramenta de dados."))
    finally:
        client.close()


if __name__ == "__main__":
    main()