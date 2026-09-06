"""Export the FastAPI schema used by the portal OpenAPI tool."""

import json
from pathlib import Path

import yaml

from main import app


OUTPUT_DIRECTORY = Path(__file__).resolve().parent


def main() -> None:
    schema = app.openapi()
    (OUTPUT_DIRECTORY / "openapi.json").write_text(
        json.dumps(schema, indent=2), encoding="utf-8"
    )
    (OUTPUT_DIRECTORY / "openapi.yaml").write_text(
        yaml.safe_dump(schema, sort_keys=False, allow_unicode=True), encoding="utf-8"
    )
    print("Wrote openapi.json and openapi.yaml")


if __name__ == "__main__":
    main()