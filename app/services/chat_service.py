from pydantic import Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.client import chat_completion
from app.ai.prompt_builder import build_system_prompt
from app.repositories.conversation_repo import ConversationRepository

import logging
from typing import List
import httpx
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.constants import ResponseCode
from app.db.session import get_db
from app.repositories.character_repo import CharacterRepository
from app.repositories.message_repo import MessageRepository
from app.schemas.chat import ChatRequest, ChatResponse, ChatMessage
from app.schemas.common import ResponseModel
from app.services.character_service import CharacterService


class ChatService:
    @staticmethod
    async def send_message(
            db: Session,
            user_id: int,
            character_id: int,
            content: str,

    ) -> str:
        try:
            # 获取或创建会话
            conversation = await ConversationRepository.get_active(
                db, user_id, character_id
            )
            if not conversation:
                conversation = await ConversationRepository.create(
                    db, user_id, character_id
                )

            # 准备消息历史记录（最近 N 条）
            history_msgs = await MessageRepository.get_messages_by_conversation(
                db, conversation.id
            )

            # 限制历史长度
            max_history = 10
            # 这句话的作用是 裁剪历史消息的长度，保证传给 LLM 的上下文不会太长
            recent_history = history_msgs[-max_history:] if len(history_msgs) > max_history else history_msgs


            message_history = [
                {
                    "role": "user" if msg.sender_type == "user" else "assistant",
                    "content": msg.content
                }
                for msg in recent_history
            ]

            # # 把当前用户输入也加入 prompt（但还不入库）
            # message_history.append({
            #     "role": "user",
            #     "content": content
            # })

            # 4️⃣ 构建 system prompt + 历史
            character =  CharacterRepository.get_by_id(db, character_id)
            messages_for_llm = build_system_prompt(character,content, message_history)

            # 4️⃣ 调用 LLM
            llm_resp = await chat_completion(messages_for_llm)

            reply = llm_resp.reply
            token_count = llm_resp.usage.total_tokens

            # 到这里才开始真正写库（事务安全）
            # 存储用户消息
            await MessageRepository.create(
                db,
                conversation_id=conversation.id,
                sender_type="user",
                content=content
            )
            # 存储助手回复
            assistant_message = await MessageRepository.create(
                db,
                conversation_id=conversation.id,
                sender_type="assistant",
                content=reply,
                token_count=token_count
            )

            # 更新会话的最后消息时间
            await ConversationRepository.touch(db, conversation)

            db.commit()
            return reply

        except Exception as e:
            db.rollback()
            # 记录日志（非常重要）
            logging.exception("send_message failed", exc_info=e)
            raise
