from pydantic import BaseModel

class ProductRequest(BaseModel):
    productName: str