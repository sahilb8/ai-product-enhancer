from langchain.tools import tool
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from app.services.vector_store import LocalEmbeddingFunction, get_chroma_client
from app.config.common import config
from langchain_google_genai import ChatGoogleGenerativeAI

@tool
def product_review_qa_tool(question: str) -> str:
    """
    Use this tool ONLY to answer questions about customer opinions, feedback, 
    likes, dislikes, and specific details mentioned in the product reviews.
    The input should be a user's complete, natural language question.
    """

    template =  """
      Answer the question based only on the following context:
      {context}
      Question: {question}
      """

    rag_chain = rag_chain_toolkit(template, question)
    return rag_chain.invoke(question)

@tool
def competitor_lookup_tool(product_name: str) -> str:
  """
  Use this tool to find the main competitors for a given product name.
  The input can be the part of the product name or the exact product name.
  """

  product_name = product_name.strip()
  
  competitors = {
      "Aero-Glide Running Shoes": ["Nike AirZoom", "Adidas Ultraboost", "Hoka Clifton"],
      "boAt Wave Neo": ["jbl", "oneplus", "sony"],
  }

  return f"The main competitors for {product_name} are: {', '.join(competitors.get(product_name, ['N/A']))}."

def rag_chain_toolkit(template: str, query: str = ""):
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

    retrieved_docs = retriever.invoke(query)
    print(f"Retrieved {len(retrieved_docs)} documents.")
    print(retrieved_docs)
    # 'RunnablePassthrough' passes the original question through unchanged.
    setup = {"context": retriever, "question": RunnablePassthrough()}
    
    prompt = ChatPromptTemplate.from_template(template)

    output_parser = StrOutputParser()

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",google_api_key=config.GEMINI_API_KEY,)

    rag_chain = setup | prompt | llm | output_parser

    return rag_chain