from fastapi import APIRouter
import httpx
from app.schemas.product import ProductRequest

router = APIRouter(prefix="/products", tags=["products"])

LLM_API_URL = "https://api.openai.com/v1/chat/completions"
API_KEY = 'your_api_key_here'  # Replace with your actual API key

@router.post("/generate-description")
async def generate_description(request: ProductRequest):
    headers = {
        "Authorization": "Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": "Generate a marketing description for {request.product_name}."}
        ]
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(LLM_API_URL, json=payload, headers=headers)
        response.raise_for_status() # Raise an exception for bad status codes
        llm_response = response.json()
        return {"description": llm_response["choices"]["message"]["content"]}
