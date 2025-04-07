# core/context_qdrant.py

from typing import List, Tuple
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from sentence_transformers import SentenceTransformer
from core.context import ContextStorage

class QdrantVectorStore(ContextStorage):
    def __init__(self, host: str = "localhost", port: int = 1010, collection_name: str = "context_collection"):
        self.client = QdrantClient(host=host, port=port)
        self.collection_name = collection_name
        self.model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

        if not self.client.collection_exists(collection_name=self.collection_name):
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )

    def add(self, text: str, metadata: dict) -> None:
        embedding = self.model.encode(text).tolist()
        self.client.upsert(
            collection_name=self.collection_name,
            points=[{
                "id": None,
                "vector": embedding,
                "payload": {"text": text, "metadata": metadata}
            }]
        )

    def search(self, query: str, top_k: int = 5) -> List[Tuple[str, float]]:
        embedding = self.model.encode(query).tolist()
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=embedding,
            limit=top_k
        )
        return [(hit.payload.get("text", ""), hit.score) for hit in search_result]
