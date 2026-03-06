


# app/services/voice_service.py

import uuid

from app.core.config import settings
from app.core.logging import get_logger
from app.services.xtts_service import xtts_service

logger = get_logger(__name__)

def create_voice(sample_path: str) -> dict:
    """
    创建声音模型 - 只保存文件，生成预览
    """
    voice_id = str(uuid.uuid4())
    print(f"创建声音: {voice_id}")

    # 1. 复制样本到永久存储
    import shutil
    audio_path = settings.VOICE_MODELS_DIR / f"{voice_id}.wav"
    audio_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(sample_path, audio_path)

    # 2. 生成预览音频 - 直接用 tts_to_file
    preview_path = settings.VOICE_MODELS_DIR / f"{voice_id}_preview.wav"
    xtts_service.tts_to_file(
        text="你好，我是你的AI助手，很高兴认识你。",
        speaker_wav=str(audio_path),
        output_path=str(preview_path),
        language="zh"
    )
    logger.info(f"预览音频已生成: {preview_path}")

    return {
        "voice_id": voice_id,
        "preview_url": f"/static/voice_models/{voice_id}_preview.wav"
    }


def generate_speech(text: str, voice_id: str) -> str:
    """
    用已创建的声音生成语音 - 直接用 tts_to_file
    """
    print(f"生成语音: voice_id={voice_id}, text={text[:20]}...")

    # 查找原始音频文件
    audio_path = settings.VOICE_MODELS_DIR / f"{voice_id}.wav"
    if not audio_path.exists():
        raise FileNotFoundError(f"Voice {voice_id} not found")

    # 生成输出文件
    output_filename = f"speech_{uuid.uuid4().hex}.wav"
    output_path = settings.AUDIO_FILES_DIR / output_filename
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 直接调用 tts_to_file - 和测试代码一样
    xtts_service.tts_to_file(
        text=text,
        speaker_wav=str(audio_path),
        output_path=str(output_path),
        language="zh"
    )

    return f"/static/audio_files/{output_filename}"