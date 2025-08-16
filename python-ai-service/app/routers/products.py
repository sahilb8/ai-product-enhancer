from fastapi import APIRouter
import httpx
from app.schemas.product import ProductRequest

router = APIRouter(prefix="/products", tags=["products"])

LLM_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
API_KEY = ''  # Replace with your actual API key

@router.post("/generate-description")
async def generate_description(request: ProductRequest):
    headers = {
        "X-goog-api-key": API_KEY,
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
        response = await client.post(LLM_API_URL, json=payload, headers=headers)
        response.raise_for_status() # Raise an exception for bad status codes
        llm_response = response.json()
        return {"description": llm_response["candidates"][0]["content"]}
