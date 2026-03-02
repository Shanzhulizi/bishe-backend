


from fastapi import APIRouter, Depends, UploadFile, File

from app.api.deps import get_current_user, get_db
from app.core.logging import get_logger

from app.schemas.chat import ChatRequest, ChatResponse
from app.schemas.voice import ASRResponse, TTSResponse, TTSRequest
from app.services.ars_service import ASRService
from app.services.chat_service import ChatService
from app.services.tts_service import TTSService

router = APIRouter()

logger = get_logger(__name__)

"""
    需要注意的是，这里的接口并不会在实际项目中直接使用，
    项目中的语音转文字和文本转语音功能会集成在聊天接口中。
    这里的接口仅作为示例，展示如何设计语音相关的 API。
    并且，这里也实现了具体的逻辑，可以更方便地测试单个功能
"""

"""
    语音转文字接口
"""
@router.post("/asr", response_model=ASRResponse)
async def voice_asr(
    audio: UploadFile = File(...),
    lang: str = "zh",
    user=Depends(get_current_user)
):
    audio_bytes = await audio.read()
    text, duration = await ASRService.speech_to_text(audio_bytes, lang)
    return {"text": text, "duration": duration}



"""
    文本转语音接口
"""
@router.post("/tts", response_model=TTSResponse)
async def voice_tts(
    req: TTSRequest,
    user=Depends(get_current_user)
):
    audio_url = await TTSService.text_to_speech(
        text=req.text,
        character_id=req.character_id,
        voice_style=req.voice_style
    )
    return {"audio_url": audio_url}