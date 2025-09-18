# src/config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Environment-Specific ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set.")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

LLM_API_URL = os.getenv("LLM_API_URL")

# --- Project Constants ---
CHROMA_DB_LANGCHAIN_PATH = "db"
LOCAL_EMBEDDING_MODEL = "all-MiniLM-L6-v2" 
COLLECTION_NAME = "product_reviews"
SOURCE_DATA_PATH = "data/flipkart_reviews.csv"