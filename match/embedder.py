from sentence_transformers import SentenceTransformer, util
import torch
from typing import List, Union

class Embedder:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        # Check if GPU is available
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = SentenceTransformer(model_name, device=self.device)

    def encode(self, texts: Union[str, List[str]]):
        """Encodes text(s) into embeddings."""
        return self.model.encode(texts, convert_to_tensor=True)

    def compute_similarity(self, query_embedding, doc_embeddings):
        """Computes cosine similarity."""
        return util.cos_sim(query_embedding, doc_embeddings)

if __name__ == "__main__":
    embedder = Embedder()
    emb1 = embedder.encode("Python programming")
    emb2 = embedder.encode("Java development")
    print(embedder.compute_similarity(emb1, emb2))
