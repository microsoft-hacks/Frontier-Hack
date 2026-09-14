"""Create and populate the electric-plant maintenance knowledge index.

Run this once per shared Azure AI Search service (facilitators only). It:
1. builds a text-search (BM25) index named ``electric-plant-maintenance``,
2. splits each markdown document in this folder into sections,
3. uploads the chunks as index documents.

Configuration (env):
- AZURE_SEARCH_ENDPOINT (required, e.g. https://<service>.search.windows.net)
- AZURE_SEARCH_ADMIN_KEY (optional; falls back to Azure CLI identity via RBAC)
- ELECTRIC_PLANT_SEARCH_INDEX (optional, default electric-plant-maintenance)

Example:
    $env:AZURE_SEARCH_ENDPOINT = "https://search-hack-shared.search.windows.net"
    python labs/electric-plant/search-knowledge/setup_index.py
"""

import os
import re
import sys
from pathlib import Path

from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchField,
    SearchableField,
    SimpleField,
    SearchIndex,
)

INDEX_NAME = os.getenv("ELECTRIC_PLANT_SEARCH_INDEX", "electric-plant-maintenance")
KNOWLEDGE_DIR = Path(__file__).resolve().parent
MAX_CHUNK_CHARS = 1100
MIN_CHUNK_CHARS = 180


def _parse_front_matter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    meta: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip()
    return meta, text[end + 4 :].strip()


def _chunk_sections(markdown: str) -> list[str]:
    """Split markdown into sections by '##' heading, keeping related prose together."""
    parts = re.split(r"(?m)^## ", markdown)
    chunks: list[str] = []
    buffer = ""
    for part in parts[1:]:
        section = "## " + part.strip()
        candidate = f"{buffer}\n\n{section}" if buffer else section
        if len(candidate) > MAX_CHUNK_CHARS and buffer:
            chunks.append(buffer.strip())
            buffer = section
        elif len(candidate) > MAX_CHUNK_CHARS:
            chunks.append(section.strip())
            buffer = ""
        else:
            buffer = candidate
    if buffer and len(buffer.strip()) >= MIN_CHUNK_CHARS:
        chunks.append(buffer.strip())
    return chunks


def build_index(index_client: SearchClient, index_name: str) -> None:
    index = SearchIndex(
        name=index_name,
        fields=[
            SimpleField(name="id", type="Edm.String", key=True, filterable=True),
            SearchableField(name="title", type="Edm.String", filterable=True),
            SearchableField(name="category", type="Edm.String", filterable=True, facetable=True),
            SearchableField(name="content", type="Edm.String"),
            SimpleField(name="source", type="Edm.String", filterable=True),
        ],
    )
    if index_name in index_client.list_index_names():
        print(f"Deleting existing index: {index_name}")
        index_client.delete_index(index_name)
    index_client.create_index(index)
    print(f"Created index: {index_name}")


def upload_documents(search_client: SearchClient, docs: list[dict]) -> None:
    result = search_client.upload_documents(docs)
    failed = [r for r in result if not r.succeeded]
    if failed:
        sys.exit(f"Upload failed for {len(failed)} chunks: {failed[:3]}")
    print(f"Uploaded {len(docs)} chunks")


def main() -> None:
    endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
    if not endpoint:
        sys.exit("AZURE_SEARCH_ENDPOINT is required (e.g. https://<service>.search.windows.net).")

    credential: AzureKeyCredential | DefaultAzureCredential
    if os.getenv("AZURE_SEARCH_ADMIN_KEY"):
        credential = AzureKeyCredential(os.getenv("AZURE_SEARCH_ADMIN_KEY"))
    else:
        credential = DefaultAzureCredential()

    docs = []
    for path in sorted(KNOWLEDGE_DIR.glob("*.md")):
        if path.name == "README.md":
            continue
        meta, body = _parse_front_matter(path.read_text(encoding="utf-8"))
        for i, chunk in enumerate(_chunk_sections(body)):
            docs.append(
                {
                    "id": f"{path.stem}-{i:03d}",
                    "title": meta.get("title", path.stem),
                    "category": meta.get("category", "geral"),
                    "content": chunk,
                    "source": f"{path.stem}.md",
                }
            )

    index_client = SearchIndexClient(endpoint=endpoint, credential=credential)
    build_index(index_client, INDEX_NAME)

    search_client = SearchClient(endpoint=endpoint, index_name=INDEX_NAME, credential=credential)
    upload_documents(search_client, docs)

    print(f"\nIndex '{INDEX_NAME}' ready.")
    print("Create the project connection (if missing) and attach the tool with:")
    print(f"  connection name : search-hack-shared")
    print(f"  index name      : {INDEX_NAME}")


if __name__ == "__main__":
    main()