"""Read-only FastAPI service for Northline Motion Works asset condition data."""

from fastapi import FastAPI, HTTPException, Path
from fastapi.openapi.utils import get_openapi

from data_store import get_asset_condition as read_asset_condition
from models import AssetCondition, ErrorResponse


app = FastAPI(
    title="Northline Motion Works Asset Condition API",
    description=(
        "Returns current readings, entity-specific thresholds, violations, and reported status "
        "for one Riverbend Electrification Plant drive."
    ),
    version="1.0.0",
    servers=[{"url": "/", "description": "Replace with the facilitator-confirmed API base URL"}],
)
app.openapi_version = "3.0.3"


@app.get(
    "/assets/{asset_id}/condition",
    operation_id="get_asset_condition",
    response_model=AssetCondition,
    summary="Get one asset's condition",
    description=(
        "Use this operation whenever an asset ID such as DRIVE-103 must be classified. "
        "It returns all four readings, that asset's thresholds, violations, and known issues."
    ),
    responses={404: {"model": ErrorResponse, "description": "Asset not found"}},
)
def get_asset_condition(
    asset_id: str = Path(..., description="Stable asset ID from DRIVE-101 through DRIVE-105"),
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