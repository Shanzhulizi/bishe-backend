from typing import List, Dict

from app.ai.local_model import local_model_chat
from app.ai.schemas import LLMResponse


async def chat_completion(messages: List[Dict]) -> LLMResponse:
    # 后期可以根据配置切换不同模型
    # return await deepseek_chat(messages)

    return await local_model_chat(messages)
