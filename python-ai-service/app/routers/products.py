from fastapi import APIRouter
import httpx
from app.config.common import config
from app.schemas.product import ProductRequest

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/generate-description")
async def generate_description(request: ProductRequest):
    headers = {
        "X-goog-api-key": config.GEMINI_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "contents": [
        {
            "parts": [
            {
                "text": "Generate a marketing description for {request.productName}."
            }
            ]
        }
        ]
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(config.LLM_API_URL, json=payload, headers=headers)
        response.raise_for_status() # Raise an exception for bad status codes
        llm_response = response.json()
        return {"description": llm_response["candidates"][0]["content"]}
