from pathlib import Path

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

DB_PATH = Path(__file__).parent / "chroma_db"
COLLECTION_NAME = "knowledge"


def get_collection():
    client = chromadb.PersistentClient(path=str(DB_PATH))
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        ),
        configuration={"hnsw": {"space": "cosine"}},
    )