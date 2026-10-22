"""Load and query the canonical industrial machine dataset."""

import json
from functools import lru_cache
from pathlib import Path


DATA_PATH = Path(__file__).resolve().parent / "data" / "api_data.json"


@lru_cache(maxsize=1)
def load_plant() -> dict:
    with DATA_PATH.open(encoding="utf-8") as data_file:
        return json.load(data_file)


def get_machines(status: str | None = None, machine_type: str | None = None) -> list[dict]:
    machines = load_plant()["readings"]
    if status is not None:
        machines = [machine for machine in machines if machine["status"] == status]
    if machine_type is not None:
        machines = [machine for machine in machines if machine["type"] == machine_type.strip().lower()]
    return machines


def get_machine(machine_id: str) -> dict | None:
    requested_id = machine_id.strip().upper()
    return next((machine for machine in load_plant()["readings"] if machine["id"] == requested_id), None)


def get_machine_list(status: str | None = None, machine_type: str | None = None) -> dict:
    plant = load_plant()
    machines = get_machines(status, machine_type)
    return {
        "company": plant["company"],
        "plant": plant["plant"],
        "timestamp": plant["timestamp"],
        "count": len(machines),
        "machines": machines,
    }


def get_plant_status() -> dict:
    plant = load_plant()
    return {key: plant[key] for key in ("company", "plant", "timestamp", "units", "summary")}
