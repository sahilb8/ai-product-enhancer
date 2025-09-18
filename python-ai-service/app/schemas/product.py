from pydantic import BaseModel

class ProductRequest(BaseModel):
    productName: str

class ProductQueryRequest(BaseModel):
    productQuery: str