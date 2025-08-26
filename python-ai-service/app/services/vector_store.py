# src/vector_store.py
import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings, Collection
from sentence_transformers import SentenceTransformer
from typing import List, Dict

# 1. Create a custom embedding function using sentence-transformers
class LocalEmbeddingFunction(EmbeddingFunction):
    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)

    def __call__(self, input: Documents) -> Embeddings:
        # The model.encode method handles batching and returns numpy arrays
        embeddings = self.model.encode(input, convert_to_numpy=True).tolist()
        return embeddings

# 2. Update the get_chroma_collection function
def get_chroma_collection(db_path: str, collection_name: str, model_name: str) -> Collection:
    """
    Initializes a ChromaDB client and returns the specified collection
    using a local sentence-transformer model.
    """
    client = chromadb.PersistentClient(path=db_path)
    
    # Use our custom local embedding function
    embedding_function = LocalEmbeddingFunction(model_name=model_name)
    
    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_function, # Pass our custom function here
        metadata={"hnsw:space": "cosine"}
    )
    return collection

# The add_to_collection function does not need to be changed.
def add_to_collection(collection: Collection, documents: List[str], metadatas: List[dict], ids: List[str]):
    collection.add(documents=documents, metadatas=metadatas, ids=ids)
    print(f"Successfully added {collection.count()} documents to the '{collection.name}' collection.")