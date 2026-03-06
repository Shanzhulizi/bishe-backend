# app/api/v1/xtts.py

import uuid

from fastapi import APIRouter, Form

from app.core.config import settings
from app.services.xtts_service import xtts_service

router = APIRouter()


@router.post("/tts")
async def generate_voice(
        text: str = Form(...),
        voice_id: str = Form(...)
):
    try:
        print(f"收到TTS请求: voice_id={voice_id}, text={text[:20]}...")

        # 查找声音文件
        sample_path = settings.VOICE_MODELS_DIR / f"{voice_id}.wav"
        if not sample_path.exists():
            return {
                "code": 404,
                "msg": f"声音不存在: {voice_id}",
                "data": None
            }

        # 确保输出目录存在
        output_dir = settings.AUDIO_FILES_DIR
        output_dir.mkdir(parents=True, exist_ok=True)

        output_filename = f"speech_{uuid.uuid4().hex}.wav"
        output_path = output_dir / output_filename

        # ✅ 改为 tts_to_file
        xtts_service.tts_to_file(
            text=text,
            speaker_wav=str(sample_path),
            output_path=str(output_path),
            language="zh"
        )

        return {
            "code": 200,
            "msg": "生成成功",
            "data": {
                "audio_url": f"/static/audio_files/{output_filename}"
            }
        }
    except Exception as e:
        print(f"TTS错误: {e}")
        import traceback
        traceback.print_exc()
        return {
            "code": 500,
            "msg": str(e),
            "data": None
        }