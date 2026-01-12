from typing import Optional

from pydantic import BaseModel, Field


class DialogueStyle(BaseModel):
    directness: float = Field(ge=0, le=1)
    verbosity: float = Field(ge=0, le=1)
    emotional_expressiveness: float = Field(ge=0, le=1)
    guidance_style: float = Field(ge=0, le=1)
    dialog_control: float = Field(ge=0, le=1)
    tolerance: float = Field(ge=0, le=1)


class Traits(BaseModel):
    bravery: float = Field(ge=0, le=1)
    kindness: float = Field(ge=0, le=1)
    logic: float = Field(ge=0, le=1)
    emotionality: float = Field(ge=0, le=1)
    curiosity: float = Field(ge=0, le=1)
    discipline: float = Field(ge=0, le=1)
    confidence: float = Field(ge=0, le=1)
    flexibility: float = Field(ge=0, le=1)


class MemoryStrategy(BaseModel):
    short_term_memory: int = Field(ge=1, le=20)
    long_term_memory: int = Field(ge=10, le=200)


class Persona(BaseModel):
    traits: Traits
    dialogue_style: DialogueStyle
    memory_strategy: MemoryStrategy


class CharacterCreate(BaseModel):
    name: str
    avatar: Optional[str] = None
    description: Optional[str] = None
    worldview: Optional[str] = None
    # voice: string
    tags: list[str] = []


class CharacterResponse(BaseModel):
    id: int
    name: str
    avatar: Optional[str] = None
    description: Optional[str] = None
    worldview: Optional[str] = None
    is_active: bool = True
    persona: Optional[Persona] = None  # 对应 CharacterConfigs.persona

    class Config:
        from_attributes = True
