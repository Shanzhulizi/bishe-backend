from pydantic import BaseModel


class ASRResponse(BaseModel):
    text: str
    duration: float


class TTSRequest(BaseModel):
    text: str
    character_id: int
    voice_style: str = "default"


class TTSResponse(BaseModel):
    audio_url: str
