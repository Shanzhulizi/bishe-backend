
from fastapi import APIRouter, Depends

from app.api.deps import get_current_user, get_db
from app.core.logging import get_logger
from app.repositories.conversation_repo import ConversationRepository
from app.repositories.message_repo import MessageRepository
import asyncio

from fastapi import APIRouter, Depends, UploadFile, File, Form

from app.api.deps import get_current_user, get_db
from app.core.logging import get_logger
from app.schemas.chat import ChatRequest, ChatResponse
from app.schemas.voice import TTSRequest
from app.services.ars_service import ASRService
from app.services.chat_service import ChatService
from app.services.tts_service import TTSService
from fastapi.responses import StreamingResponse
router = APIRouter()
router = APIRouter()

# @router.get("/recommendations/popular")
# async def get_popular_characters(
#         limit: int = 10,
#         db: Session = Depends(get_db)
# ):
#     """获取热门角色推荐"""
#     characters = db.query(Character).order_by(
#         desc(Character.popularity_score)
#     ).limit(limit).all()
#
#     return [
#         {
#             "id": char.id,
#             "name": char.name,
#             "avatar": char.avatar,
#             "tags": char.tags,
#             "stats": {
#                 "usage": char.usage_count,
#                 "recent_usage": char.recent_usage_count,
#                 "likes": char.like_count,
#                 "chats": char.chat_count,
#                 "popularity": char.popularity_score
#             }
#         }
#         for char in characters
#     ]