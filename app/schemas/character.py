from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class CharacterBase(BaseModel):
    name: str
    description: Optional[str] = None
    personality: str
    background: Optional[str] = None
    greeting_message: str
    example_dialogue: Optional[str] = None
    initial_prompt: str
    avatar_url: Optional[str] = None
    tags: Optional[List[str]] = None
    is_public: bool = True


class CharacterCreate(CharacterBase):
    pass


class CharacterResponse(CharacterBase):
    id: int
    created_by: int
    usage_count: int
    rating: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True