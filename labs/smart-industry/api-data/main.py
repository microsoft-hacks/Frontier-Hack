"""Read-only FastAPI service for Smart Industry machine data."""

from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.openapi.utils import get_openapi

from data_store import (
    get_machine as read_machine,
    get_machine_list as read_machine_list,
    get_plant_status as read_plant_status,
)
from models import ErrorResponse, Machine, MachineList, MachineStatus, PlantStatus


app = FastAPI(
    title="API de Máquinas Industriais — Smart Industry",
    description=(
        "Retorna telemetria atual, parâmetros operacionais, status, motivos e alertas "
        "das máquinas da Unidade Industrial SP."
    ),
    version="1.1.0",
    servers=[{"url": "/", "description": "Substitua pela URL base da API confirmada pelo facilitador"}],
)
app.openapi_version = "3.0.3"


@app.get(
    "/plant/status",
    operation_id="get_plant_status",
    response_model=PlantStatus,
    response_model_exclude_none=True,
    summary="Obtém o resumo da planta",
    description=(
        "Retorna o resumo de máquinas por status (online, alert, offline), os IDs em alerta e offline "
        "e as unidades de cada campo."
    ),
)
def get_plant_status() -> dict:
    return read_plant_status()


@app.get(
    "/machines",
    operation_id="list_machines",
    response_model=MachineList,
    response_model_exclude_none=True,
    summary="Lista as máquinas",
    description=(
        "Retorna a telemetria, os parâmetros, o status, os motivos e os alertas de todas as máquinas. "
        "Use os filtros opcionais status e type para restringir o resultado."
    ),
)
def list_machines(
    status: MachineStatus | None = Query(None, description="Filtra por status: online, alert ou offline."),
    type: str | None = Query(
        None, description="Filtra por tipo: cnc, robot, conveyor, forklift, injector, press ou welder."
    ),
) -> dict:
    return read_machine_list(status.value if status else None, type)


@app.get(
    "/machines/{machine_id}",
    operation_id="get_machine",
    response_model=Machine,
    response_model_exclude_none=True,
    summary="Obtém uma máquina",
    description=(
        "Use esta operação sempre que um ID de máquina como CNC-003 precisar ser analisado. "
        "Ela retorna telemetria, parâmetros com limites, status, motivos e alertas."
    ),
    responses={404: {"model": ErrorResponse, "description": "Máquina não encontrada"}},
)
def get_machine(
    machine_id: str = Path(..., description="ID da máquina (por exemplo CNC-003, ROB-003, CVY-003, INJ-002)"),
) -> dict:
    machine = read_machine(machine_id)
    if machine is None:
        raise HTTPException(status_code=404, detail=f"Machine '{machine_id}' not found")
    return machine


def _to_openapi_30(node):
    """Rewrite OpenAPI 3.1 nullable unions (anyOf with type null) into valid 3.0.3 constructs."""
    if isinstance(node, list):
        return [_to_openapi_30(item) for item in node]
    if not isinstance(node, dict):
        return node
    node = {key: _to_openapi_30(value) for key, value in node.items()}
    options = node.get("anyOf")
    if isinstance(options, list) and any(option == {"type": "null"} for option in options):
        remaining = [option for option in options if option != {"type": "null"}]
        if len(remaining) == 1:
            if "$ref" in remaining[0]:
                return remaining[0]
            rest = {key: value for key, value in node.items() if key != "anyOf"}
            return {**remaining[0], **rest}
        node["anyOf"] = remaining
    return node


def custom_openapi() -> dict:
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
        servers=app.servers,
        openapi_version=app.openapi_version,
    )
    app.openapi_schema = _to_openapi_30(schema)
    return app.openapi_schema


app.openapi = custom_openapi
