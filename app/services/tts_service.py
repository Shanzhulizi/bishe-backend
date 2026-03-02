import uuid
import os
import edge_tts
from app.core.config import settings

# 常用中文角色（可按 character 绑定）
VOICE_MAP = {
    "default": "zh-CN-XiaoxiaoNeural",
    "male": "zh-CN-YunxiNeural",
    "calm": "zh-CN-XiaoyiNeural",
}


class TTSService:

    @staticmethod
    async def text_to_speech(
            text: str,
            character_id: int,
            voice_style: str = "default"
    ) -> str:
        """
        返回音频 URL
        """
        try:

            voice = VOICE_MAP.get(voice_style, VOICE_MAP["default"])

            filename = f"{uuid.uuid4().hex}.mp3"
            save_dir = os.path.join(settings.STATIC_DIR, "tts")

            os.makedirs(save_dir, exist_ok=True)

            file_path = os.path.join(save_dir, filename)

            communicate = edge_tts.Communicate(
                text=text,
                voice=voice,
                rate="+0%",
                volume="+0%"
            )

            await communicate.save(file_path)

            # return f"/static/tts/{filename}"
            return f"http://localhost:8000/static/tts/{filename}"
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise e