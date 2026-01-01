from pydantic import BaseModel
from typing import Optional, Dict


class CharacterCreate(BaseModel):
    name: str
    description: Optional[str] = None
    worldview: Optional[str] = None
    speech_style: Optional[str] = None
    persona: Dict  # JSONB 存储角色人格配置


class CharacterResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    worldview: Optional[str] = None
    speech_style: Optional[str] = None
    is_active: bool
    persona: Optional[Dict] = None  # 对应 CharacterConfigs.persona

    class Config:
        orm_mode = True  # 支持从 ORM 模型直接生成 Pydantic 对象
