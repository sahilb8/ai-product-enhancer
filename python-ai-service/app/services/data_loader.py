# src/data_loader.py
import pandas as pd
from typing import List, Dict, Tuple

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
        # Assuming the relevant columns are 'product_name' and 'Review'
        df_clean = df.dropna(subset=['product_name', 'Review']).copy()
        df_clean['document'] = df_clean['product_name'] + ". Review: " + df_clean['Review']
        return df_clean.sample(n=sample_size, random_state=42)
    except FileNotFoundError:
        print(f"Error: '{file_path}' not found. Please check the path.")
        raise
    except KeyError as e:
        print(f"Error: Missing expected column in CSV: {e}")
        raise


def transform_for_chroma(df: pd.DataFrame) -> Tuple[List[str], List[Dict], List[str]]:
    """
    Transforms a DataFrame into the lists required by ChromaDB.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        Tuple containing lists of documents, metadatas, and ids.
    """
    documents = df['document'].tolist()
    # Select desired columns for metadata
    metadatas = df[['product_name', 'Rate']].to_dict('records')
    ids = [f"review_{i}" for i in range(len(documents))]
    return documents, metadatas, ids