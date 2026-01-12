import logging
from typing import List
import httpx
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.config import settings
from app.core.constants import ResponseCode
from app.repositories.character_repo import CharacterRepository
from app.schemas.chat import ChatRequest, ChatResponse
from app.schemas.common import ResponseModel
from app.services.character_service import CharacterService
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
