from pydantic import BaseModel


class AgentQueryRequest(BaseModel):
    agentQuery: str