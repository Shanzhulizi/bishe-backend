# app/api/v1/cosyvoice.py

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import uuid
import shutil
from pathlib import Path

# from app.services.cosyvoice_service import cosyvoice_service
from app.core.config import settings
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


# @app.post("/voice/generate", summary="生成角色语音")
# async def generate_voice(request: RoleVoiceRequest):
#     """生成角色语音"""
#     try:
#         file_path = voice_service.generate_speech(
#             request.role_id,
#             request.text,
#             request.filename
#         )
#
#         # 获取音频时长
#         import soundfile as sf
#         audio, sr = sf.read(file_path)
#         duration = len(audio) / sr
#
#         return VoiceResponse(
#             success=True,
#             message="生成成功",
#             file_path=file_path,
#             duration=duration
#         )
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
#
#
# @router.post("/speak")
# async def speak(
#         text: str = Form(...),
#         voice_id: str = Form(...)
# ):
#     """
#     用 CosyVoice 生成语音
#     """
#     try:
#         audio_url = cosyvoice_service.generate_speech(text, voice_id)
#
#         return {
#             "code": 200,
#             "msg": "生成成功",
#             "data": {
#                 "audio_url": audio_url
#             }
#         }
#     except FileNotFoundError:
#         return {
#             "code": 404,
#             "msg": "声音不存在",
#             "data": None
#         }
#     except Exception as e:
#         logger.error(f"生成失败: {e}")
#         return {
#             "code": 500,
#             "msg": str(e),
#             "data": None
#         }
