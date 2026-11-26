import json
from pathlib import Path

from store import DB_PATH, get_collection

DOCS_PATH = Path(__file__).parent / "docs.json"

docs = json.loads(DOCS_PATH.read_text(encoding="utf-8"))
collection = get_collection()

collection.upsert(
    ids=[d["id"] for d in docs],
    documents=[d["text"] for d in docs],
    metadatas=[{"topic": d["topic"], "source": d["source"]} for d in docs],
)

print(f"Stored {collection.count()} documents in {DB_PATH}")