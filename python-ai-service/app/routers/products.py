from fastapi import APIRouter
from langchain_google_genai import ChatGoogleGenerativeAI

from app.config.common import config
from app.schemas.product import ProductDescription, ProductRequest, ProductQueryRequest
from app.services.agent_tool import rag_chain_toolkit


router = APIRouter(prefix="/products", tags=["products"])

@router.post("/generate-description")
async def generate_description(request: ProductRequest):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",google_api_key=config.GEMINI_API_KEY,)
    structured_llm = llm.with_structured_output(ProductDescription)

    prompt_text = f"Generate marketing copy for {request.productName}."

    structured_response = structured_llm.invoke(prompt_text)

    return structured_response
    
@router.post("/answer-product-query")
async def answer_product_query(request: ProductQueryRequest):
    template =  """
        Answer the question based only on the following context:
        {context}
        Question: {question}
        """
    
    rag_chain = rag_chain_toolkit(template)

    answer = rag_chain.invoke(request.productQuery)
    return {"answer": answer}
