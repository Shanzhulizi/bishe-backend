

from fastapi import APIRouter, Depends, UploadFile, File, Form

from app.api.deps import get_current_user, get_db
from app.core.logging import get_logger


from app.schemas.chat import ChatRequest, ChatResponse
from app.services.ars_service import ASRService
from app.services.chat_service import ChatService
from app.services.tts_service import TTSService

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





@router.post("/voice")
async def voice_chat(
    character_id: int= Form(...),
    audio: UploadFile = File(...),
    user=Depends(get_current_user),
    db=Depends(get_db)
):
    # 1. ASR
    audio_bytes = await audio.read()
    logger.info(f"用户 {user.id} 发送语音消息给角色 {character_id}")
    logger.info(f"语音文件大小: {len(audio_bytes)} 字节")
    logger.info(f"语音文件: {audio_bytes[:20]}...")
    try:
        user_text, _ = await ASRService.speech_to_text(audio_bytes)
    except Exception as e:
        print("ASR 失败", e)
        return {
            "user_text": "",
            "reply_text": "抱歉，我的语音识别暂时无法使用，请稍后再试",
            "audio_url": None
        }
    logger.info(f"ASR 识别结果: {user_text}")
    # 2. 聊天（你现有逻辑）
    reply_text = await ChatService.send_message(
        db=db,  # 这里接你真实 db
        user_id=user.id,
        #     user_id=1,  # 临时用一个固定用户 ID
        character_id=character_id,
        content=user_text
    )
    logger.info(f"角色 {character_id} 回复用户 {user.id} 消息: {reply_text}")
    # 3. TTS
    audio_url = await TTSService.text_to_speech(
        text=reply_text,
        character_id=character_id
    )
    logger.info(f"TTS 生成语音 URL: {audio_url}")
    return {
        "user_text": user_text,
        "reply_text": reply_text,
        "audio_url": audio_url
    }

