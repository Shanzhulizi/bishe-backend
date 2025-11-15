from fastapi import APIRouter, Depends, HTTPException
from typing import List

from openai.types.conversations import Conversation

from app.database.session import get_db
from app.models.character import Character
from app.schemas.chat import ChatRequest, ChatResponse, ConversationCreate, ConversationResponse
from app.services.chat_service import ChatService
# from app.services.llm_client import LLMClient


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.models.character import Character
from app.models.user import User  # 添加User模型导入
from app.schemas.chat import ChatRequest, ChatResponse, ConversationCreate, ConversationResponse
from app.services.chat_service import ChatService
from app.api.deps import get_current_user  # 添加认证依赖导入



router = APIRouter()
chat_service = ChatService()


async def create_conversation(
        conversation: ConversationCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """创建新对话"""
    try:
        # 创建新会话
        db_conversation = Conversation(
            user_id=current_user.id,
            character_id=conversation.character_id,
            title=conversation.title or "新对话"
        )

        db.add(db_conversation)
        db.commit()
        db.refresh(db_conversation)

        return ConversationResponse(
            id=db_conversation.id,
            title=db_conversation.title,
            character_id=db_conversation.character_id,
            message_count=db_conversation.message_count,
            last_message_at=db_conversation.last_message_at,
            created_at=db_conversation.created_at
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"创建对话失败: {str(e)}")




@router.post("/send", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """发送消息给AI角色"""
    try:
        # 1. 从数据库获取真实的角色数据
        character = db.query(Character).filter(Character.id == request.character_id).first()
        if not character:
            raise HTTPException(status_code=404, detail="角色不存在")

        # 2. 检查权限：要么是公开角色，要么是创建者本人
        if not character.is_public and character.created_by != current_user.id:
            raise HTTPException(status_code=403, detail="无权访问此角色")

        # 3. 构建角色数据
        character_data = {
            "name": character.name,
            "personality": character.personality,
            "background": character.background,
            "greeting_message": character.greeting_message,
            "initial_prompt": character.initial_prompt
        }

        # 4. 处理消息
        response = await chat_service.process_message(request, character_data)

        # 5. 更新角色使用次数（可选）
        character.usage_count += 1
        db.commit()

        return response

    except HTTPException:
        # 重新抛出HTTP异常
        raise
    except Exception as e:
        db.rollback()  # 发生异常时回滚
        raise HTTPException(status_code=500, detail=f"聊天处理失败: {str(e)}")



@router.get("/conversations/{conversation_id}/messages")
async def get_conversation_messages(conversation_id: int):
    """获取对话历史消息"""
    # 实现获取消息历史的逻辑
    return []