import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any
import uuid

class VectorIndex:
    def __init__(self, persist_directory="./aisiem_vectors"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(name="events")

    def add_events(self, ids: List[str], embeddings: List[List[float]], metadatas: List[Dict[str, Any]], documents: List[str]):
        if not ids:
            return
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=documents
        )

    def search(self, query_embedding: List[float], n_results: int = 5):
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

    def search_by_text(self, query_text: str, n_results: int = 5):
        # Chroma handles embedding automatically if we don't provide it, 
        # but we are using a custom embedder in the pipeline. 
        # For simplicity here, we assume the caller handles embedding or we rely on Chroma's default if configured.
        # However, to keep it consistent with our custom embedder, this method might need the embedding passed in.
        # We will implement the embedding generation in the Service layer.
        pass

# Global instance
vector_index = VectorIndex()
