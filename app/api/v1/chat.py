

from fastapi import APIRouter, Depends

from app.api.deps import get_current_user, get_db
from app.core.logging import get_logger

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter()

logger = get_logger(__name__)

@router.post("/send", response_model=ChatResponse)
async def send_chat(
        req: ChatRequest,
        db=Depends(get_db),
        user=Depends(get_current_user)
):
    logger.info(f"用户 {user.id} 发送消息给角色 {req.character_id}")
    reply = await ChatService.send_message(
        db=db,
        user_id=user.id,
        character_id=req.character_id,
        content=req.message,
    )
    logger.info(f"角色 {req.character_id} 回复用户 {user.id} 消息")
    return {"reply": reply
            }
