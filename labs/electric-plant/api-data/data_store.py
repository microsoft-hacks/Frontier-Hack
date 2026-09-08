"""Load and classify the canonical industrial asset dataset."""

import json
from functools import lru_cache
from pathlib import Path


DATA_PATH = Path(__file__).resolve().parent / "data" / "industrial_asset_data.json"


@lru_cache(maxsize=1)
def load_plant() -> dict:
    with DATA_PATH.open(encoding="utf-8") as data_file:
        return json.load(data_file)


def get_assets() -> list[dict]:
    return load_plant()["assets"]


def get_asset(asset_id: str) -> dict | None:
    requested_id = asset_id.strip().upper()
    return next((asset for asset in get_assets() if asset["asset_id"] == requested_id), None)


def get_asset_condition(asset_id: str) -> dict | None:
    asset = get_asset(asset_id)
    if asset is None:
        return None

    metrics = {}
    violations = []
    for metric_name, reading in asset["readings"].items():
        threshold = asset["thresholds"][metric_name]
        in_range = threshold["min"] <= reading["value"] <= threshold["max"]
        metrics[metric_name] = {
            **reading,
            **threshold,
            "in_range": in_range,
        }
        if not in_range:
            violations.append(metric_name)

    return {
        "asset_id": asset["asset_id"],
        "name": asset["name"],
        "reported_status": asset["status"],
        "metrics": metrics,
        "violations": violations,
        "issues": asset["issues"],
    }