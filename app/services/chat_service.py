from typing import List, Optional
from app.schemas.chat import ChatMessage, ChatRequest, ChatResponse
from app.services.llm_client import LLMClient
import logging

logger = logging.getLogger(__name__)


class ChatService:
    def __init__(self):
        self.llm_client = LLMClient()

    async def process_message(self, request: ChatRequest, character_data: dict) -> ChatResponse:
        """处理用户消息并返回角色回复"""
        try:
            logger.info(f"处理消息，角色: {character_data['name']}, 用户消息长度: {len(request.message)}")

            # 构建角色设定系统提示
            system_prompt = self._build_system_prompt(character_data)

            # 构建对话历史
            messages = self._build_messages(system_prompt, request.message, request.conversation_history)

            # 调用LLM
            reply = await self.llm_client.generate_response(messages)

            logger.info(f"消息处理完成，回复长度: {len(reply)}")

            return ChatResponse(
                reply=reply,
                character_id=request.character_id
            )

        except Exception as e:
            logger.error(f"处理消息时发生错误: {e}")
            # 返回一个友好的错误消息
            return ChatResponse(
                reply=f"抱歉，{character_data['name']}暂时无法回复。请稍后重试。",
                character_id=request.character_id
            )

    def _build_system_prompt(self, character: dict) -> str:
        """构建角色设定系统提示"""
        prompt = f"""
        # 角色设定
        你正在扮演{character['name']}，请完全沉浸在这个角色中。

        ## 角色性格
        {character['personality']}

        ## 背景故事  
        {character['background']}

        ## 初始问候
        {character.get('greeting_message', '')}

        ## 核心指令
        1. **严格保持角色一致性**：所有回复都必须符合角色的性格和背景设定
        2. **自然对话**：使用生动、自然的语言，避免机械感
        3. **深度沉浸**：忘记你是AI助手，完全成为这个角色
        4. **适当长度**：回复长度适中，保持对话流畅性
        5. **情感表达**：根据角色性格适当表达情感

        ## 对话风格
        {character.get('initial_prompt', '请按照角色设定自然对话')}

        现在开始，你就是{character['name']}，请开始与用户对话。
        """
        return prompt.strip()

    def _build_messages(self, system_prompt: str, user_message: str, history: Optional[List[ChatMessage]]) -> List[
        dict]:
        """构建LLM消息格式"""
        messages = [{"role": "system", "content": system_prompt}]

        # 添加历史对话
        if history:
            for msg in history[-6:]:  # 限制历史长度，节省token
                messages.append({"role": msg.role, "content": msg.content})

        # 添加当前用户消息
        messages.append({"role": "user", "content": user_message})

        logger.info(f"构建消息完成，总消息数: {len(messages)}")

        return messages