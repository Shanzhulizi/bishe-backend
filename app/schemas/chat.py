from pydantic import BaseModel
from typing import List, Optional, Literal

"""
请求模型
"""
class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str


class ChatRequest(BaseModel):
    character_id: int
    message: str
    history: Optional[List[ChatMessage]] = []


"""
响应模型
"""
class ChatResponse(BaseModel):
    reply: str
    usage: Optional[dict] = None
