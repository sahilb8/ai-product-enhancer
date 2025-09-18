# ingest.py
import random
from app.config.common import config
from app.services.vector_store import LocalEmbeddingFunction

from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from app.services.data_loader import load_and_prepare_data

def main():
    """
    Main function to orchestrate the data ingestion pipeline using LangChain.
    """
    print("--- Starting Data Ingestion Pipeline ---")

    # 1. Load and prepare data from the source file
    print(f"Step 1: Loading and preparing data from {config.SOURCE_DATA_PATH}...")
    documents = load_and_prepare_data(config.SOURCE_DATA_PATH, sample_size=3000)

    # 2. Split documents into chunks
    print("Step 2: Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    docs = text_splitter.split_documents(documents)
    print(f"\nSuccessfully splitted {len(docs)} document chunks.")

    # 3. Initialize embedding function
    print(f"Step 3: Initializing embedding model '{config.LOCAL_EMBEDDING_MODEL}'...")
    embedding_function = LocalEmbeddingFunction(model_name=config.LOCAL_EMBEDDING_MODEL)

    # 4. Create and populate the LangChain Chroma vector store
    print(f"Step 4: Creating vector store at '{config.CHROMA_DB_LANGCHAIN_PATH}'...")
    # This single command creates the client, collection, and adds the documents.
    try:
        db = Chroma.from_documents(
            documents=docs,
            embedding=embedding_function,
            persist_directory=config.CHROMA_DB_LANGCHAIN_PATH,
            collection_name=config.COLLECTION_NAME,
    )
    except (FileNotFoundError, KeyError):
        print("--- Pipeline failed at data loading step. Exiting. ---")
        return
    

    # 5. Report success using the 'docs' list we just processed
    print(f"\nSuccessfully added {len(docs)} document chunks to the collection.")
    print("--- Data Ingestion Pipeline Finished Successfully ---")

if __name__ == "__main__":
    main()