# src/data_loader.py
import pandas as pd
from langchain.schema import Document
from app.config.common import config

def load_and_prepare_data(file_path: str, sample_size: int = 500) -> pd.DataFrame:
    """
    Loads data from a CSV, cleans it, and returns a sampled DataFrame.

    Args:
        file_path (str): The path to the source CSV file.
        sample_size (int): The number of samples to return.

    Returns:
        pd.DataFrame: A cleaned and sampled pandas DataFrame.
    """
    try:
        df = pd.read_csv(file_path)
        df_clean = df.dropna(subset=['product_name', 'Review']).copy()
        # Sample the data *before* creating documents for efficiency
        df_sampled = df_clean.sample(n=sample_size, random_state=42)
        df_sampled['page_content'] = df_sampled['product_name'] + ". Review: " + df_sampled['Review']
    
        # Create a list of Document objects
        documents = []
        for _, row in df_sampled.iterrows():
            # Define what goes into the metadata
            metadata = {
                "product_name": row['product_name'],
                "rating": row.get('Rate', 'N/A'),
                "source": config.SOURCE_DATA_PATH
            }
            doc = Document(page_content=row['page_content'], metadata=metadata)
            documents.append(doc)

            return documents
    except (FileNotFoundError, KeyError) as e:
        print(f"Error during data loading: {e}")
        return