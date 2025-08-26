# ingest.py
from app.config.common import config
from app.services.data_loader import load_and_prepare_data, transform_for_chroma
from app.services.vector_store import get_chroma_collection, add_to_collection

def main():
    """
    Main function to orchestrate the data ingestion pipeline.
    """
    print("--- Starting Data Ingestion Pipeline ---")

    # 1. Initialize ChromaDB collection
    print("Step 1: Initializing ChromaDB collection...")
    collection = get_chroma_collection(
        db_path=config.CHROMA_DB_PATH,
        collection_name=config.COLLECTION_NAME,
        model_name=config.LOCAL_EMBEDDING_MODEL # Pass the local model name
    )

    # 2. Load and prepare data from the source file
    print("Step 2: Loading and preparing data from {config.SOURCE_DATA_PATH}...")
    try:
        reviews_df = load_and_prepare_data(config.SOURCE_DATA_PATH)
    except (FileNotFoundError, KeyError):
        print("--- Pipeline failed at data loading step. Exiting. ---")
        return

    # 3. Transform data into ChromaDB format
    print("Step 3: Transforming data for ChromaDB...")
    documents, metadatas, ids = transform_for_chroma(reviews_df)

    # 4. Add data to the collection
    print("Step 4: Adding data to the collection...")
    add_to_collection(
        collection=collection,
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    
    print("--- Data Ingestion Pipeline Finished Successfully ---")

if __name__ == "__main__":
    main()