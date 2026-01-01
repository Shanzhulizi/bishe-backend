import logging

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.character import CharacterCreate
from app.schemas.character import CharacterResponse
from app.services.character_service import CharacterService
from app.repositories.character_repo import CharacterRepository

router = APIRouter()
service = CharacterService(CharacterRepository())


@router.post("/create", response_model=CharacterResponse)
def create_character(data: CharacterCreate, db: Session = Depends(get_db)):
    char = service.create_character(db, data)
    logging.info(f"创建角色成功: {char.id} - {char.name}")
    return {
        "id": char.id,
        "name": char.name,
        "description": char.description,
        "worldview": char.worldview,
        "is_active": True ,
        "speech_style": char.speech_style,
        "persona": char.config.persona if char.config else {}

    }
