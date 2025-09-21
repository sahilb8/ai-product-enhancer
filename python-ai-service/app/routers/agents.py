from fastapi import APIRouter
from langchain_google_genai import ChatGoogleGenerativeAI
from app.schemas.agent import AgentQueryRequest
from langchain.agents import create_react_agent, AgentExecutor
from langchain.memory import ConversationBufferWindowMemory
from app.services.agent_tool import product_review_qa_tool, competitor_lookup_tool
from app.config.common import config
from langchain import hub


router = APIRouter(prefix="/agents", tags=["agents"])

@router.post("/answer-agent-query")
async def agent_query(request: AgentQueryRequest):
  tools = [product_review_qa_tool, competitor_lookup_tool]

  # 2. Set up conversational memory to remember past interactions
  memory = ConversationBufferWindowMemory(k=5) # Remembers last 5 turns

  llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",google_api_key=config.GEMINI_API_KEY,)

  prompt = hub.pull("hwchase17/react")

  # 3. Create the agent with a system prompt to guide its persona and behavior
  # The prompt should also include placeholders for chat_history and agent_scratchpad
  agent = create_react_agent(llm, tools, prompt) # Using a prompt that supports memory

  agent_executor = AgentExecutor(
      agent=agent,
      tools=tools,
      memory=memory,
      verbose=True,
      handle_parsing_errors=True # Makes the agent more robust
  )
  # The agent_executor now uses the memory to handle conversational context
  response = await agent_executor.ainvoke({"input": request.agentQuery})
  return {"response": response["output"]}
