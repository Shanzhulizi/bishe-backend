from typing import List, Dict
from app.ai.schemas import LLMResponse
from app.ai.deepseek import deepseek_chat

async def chat_completion(messages: List[Dict]) -> LLMResponse:
    # 后期可以根据配置切换不同模型
    return await deepseek_chat(messages)
