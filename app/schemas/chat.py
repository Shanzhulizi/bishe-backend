from pydantic import BaseModel
from typing import List, Optional

class ChatMessage(BaseModel):
    role: str  # user 或 assistant
    content: str

class ChatRequest(BaseModel):
    character_id: int
    message: str
    conversation_history: Optional[List[ChatMessage]] = None

class ChatResponse(BaseModel):
    reply: str
    character_id: int
    message_id: Optional[int] = None  # 暂时设为可选

class ConversationCreate(BaseModel):
    character_id: int
    title: str

class ConversationResponse(BaseModel):
    id: int
    title: str
    character_id: int