from sentence_transformers import SentenceTransformer
from typing import List

class Embedder:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        print(f"Loading embedding model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        print("Model loaded.")

    def embed_text(self, texts: List[str]) -> List[List[float]]:
        embeddings = self.model.encode(texts)
        return embeddings.tolist()

    def event_to_text(self, event) -> str:
        # Create a semantic string representation of the event
        return f"{event.ts} {event.source} {event.category} {event.subtype} {event.principal} {event.object} {event.raw}"

# Global instance
embedder_instance = Embedder()
