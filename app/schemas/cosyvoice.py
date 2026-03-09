from typing import Optional

from pydantic import BaseModel


class CosyVoiceCreateRequest(BaseModel):
    voice_text: str  # 参考音频的文本内容
    voice_wav: str  # 参考音频的文件路径或 URL


class CosyVoiceCreateResponse(BaseModel):
    pass
