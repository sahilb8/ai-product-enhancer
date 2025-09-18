from fastapi import APIRouter
import httpx
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from app.config.common import config
from app.schemas.product import ProductRequest, ProductQueryRequest
from app.services.vector_store import LocalEmbeddingFunction, get_chroma_client

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
    
@router.post("/answer-product-query")
async def answer_product_query(request: ProductQueryRequest):
    template =  """
        Answer the question based only on the following context:
        {context}
        Question: {question}
        """
    
    chroma_client = get_chroma_client(
        db_path=config.CHROMA_DB_LANGCHAIN_PATH,
    )

    embedding_function = LocalEmbeddingFunction(model_name=config.LOCAL_EMBEDDING_MODEL)

    langchain_vector_store = Chroma(
        client=chroma_client,
        collection_name=config.COLLECTION_NAME,
        embedding_function=embedding_function,
    )
    retriever = langchain_vector_store.as_retriever()

    retrieved_docs = retriever.invoke(request.productQuery)
    print(f"Retrieved {len(retrieved_docs)} documents.")
    print(retrieved_docs)
    # 'RunnablePassthrough' passes the original question through unchanged.
    setup = {"context": retriever, "question": RunnablePassthrough()}

    print(setup)

    
    prompt = ChatPromptTemplate.from_template(template)

    output_parser = StrOutputParser()

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",google_api_key=config.GEMINI_API_KEY,)

    rag_chain = setup | prompt | llm | output_parser

    answer = rag_chain.invoke(request.productQuery)
    return {"answer": answer}
