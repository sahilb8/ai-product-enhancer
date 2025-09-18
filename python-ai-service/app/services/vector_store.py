# src/vector_store.py
import chromadb
from chromadb import Collection
from sentence_transformers import SentenceTransformer
from typing import List

# 1. Create a custom embedding function using sentence-transformers
class LocalEmbeddingFunction:
    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)
        # We no longer need the .name attribute or method for LangChain
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        The method LangChain's Chroma wrapper will call for embedding
        a list of documents during ingestion.
        """
        return self.model.encode(texts, convert_to_numpy=True,show_progress_bar=True).tolist()

    def embed_query(self, text: str) -> List[float]:
        """
        The method LangChain's Chroma wrapper will call for embedding
        a single query.
        """
        return self.model.encode(text, convert_to_numpy=True).tolist()

# 2. Update the get_chroma_client function
def get_chroma_client(db_path: str) -> Collection:
    """
    Initializes a ChromaDB client and returns the specified collection
    using a local sentence-transformer model.
    """
    client = chromadb.PersistentClient(path=db_path)
    return client