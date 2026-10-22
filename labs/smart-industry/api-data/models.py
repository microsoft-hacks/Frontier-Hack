"""Typed API models for the fictional Electric Plant scenario."""

from enum import Enum

from pydantic import BaseModel, Field


class AssetStatus(str, Enum):
    normal = "normal"
    warning = "warning"
    critical = "critical"


class Reading(BaseModel):
    value: float
    unit: str


class Threshold(BaseModel):
    min: float
    max: float


class Asset(BaseModel):
    asset_id: str
    name: str
    status: AssetStatus
    readings: dict[str, Reading]
    thresholds: dict[str, Threshold]
    issues: list[str]


class PlantSnapshot(BaseModel):
    company: str
    site: str
    timestamp: str
    assets: list[Asset]


class MetricCondition(BaseModel):
    value: float
    unit: str
    min: float
    max: float
    in_range: bool


class AssetCondition(BaseModel):
    asset_id: str
    name: str
    reported_status: AssetStatus
    metrics: dict[str, MetricCondition]
    violations: list[str]
    issues: list[str]


class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Human-readable error message.")