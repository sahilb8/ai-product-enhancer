from typing import List
from pydantic import BaseModel, Field

class Product(BaseModel):
    """A Pydantic model to represent structured product data."""
    title: str = Field(description="A creative and catchy title for the product.")
    description: str = Field(description="A detailed, engaging marketing description.")
    key_features: List[str] = Field(description="A list of 3-5 key selling points or features.")

class ProductDescription(BaseModel):
    catchy_headline: str = Field(description="A short, attention-grabbing headline for the product.")
    short_summary: str = Field(description="A one-paragraph summary of the product.")
    key_features: List[str] = Field(description="A bulleted list of the top 3-5 features.")

class ProductRequest(BaseModel):
    productName: str

class ProductQueryRequest(BaseModel):
    productQuery: str