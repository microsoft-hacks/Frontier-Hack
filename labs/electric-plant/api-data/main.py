"""Read-only FastAPI service for Eletroforça Indústrias Elétricas asset condition data."""

from fastapi import FastAPI, HTTPException, Path
from fastapi.openapi.utils import get_openapi

from data_store import get_asset_condition as read_asset_condition
from models import AssetCondition, ErrorResponse


app = FastAPI(
    title="API de Condição de Ativos — Eletroforça Indústrias Elétricas",
    description=(
        "Retorna leituras atuais, limites específicos do ativo, violações e status reportado "
        "para um ativo do Complexo Industrial Serrana."
    ),
    version="1.0.0",
    servers=[{"url": "/", "description": "Substitua pela URL base da API confirmada pelo facilitador"}],
)
app.openapi_version = "3.0.3"


@app.get(
    "/assets/{asset_id}/condition",
    operation_id="get_asset_condition",
    response_model=AssetCondition,
    summary="Obtém a condição de um ativo",
    description=(
        "Use esta operação sempre que um ID de ativo como XFR-401 precisar ser classificado. "
        "Ela retorna as quatro leituras, os limites específicos do ativo, as violações e os problemas conhecidos."
    ),
    responses={404: {"model": ErrorResponse, "description": "Ativo não encontrado"}},
)
def get_asset_condition(
    asset_id: str = Path(..., description="ID do ativo permanente (MOTOR-201, GEN-301, XFR-401, DRIVE-101, VFD-501)"),
) -> dict:
    condition = read_asset_condition(asset_id)
    if condition is None:
        raise HTTPException(status_code=404, detail=f"Asset '{asset_id}' not found")
    return condition


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
    app.openapi_schema = schema
    return schema


app.openapi = custom_openapi