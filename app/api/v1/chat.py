from fastapi import APIRouter, Depends

from app.api.deps import get_current_user, get_db
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter()


@router.post("/send", response_model=ChatResponse)
async def send_chat(
        req: ChatRequest,
        db=Depends(get_db),
        user=Depends(get_current_user)
):
    reply = await ChatService.send_message(
        db=db,
        user_id=user.id,
        character_id=req.character_id,
        content=req.message,
    )
    return {"reply": reply
            }
