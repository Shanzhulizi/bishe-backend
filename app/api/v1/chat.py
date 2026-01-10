import logging

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.character import CharacterCreate
from app.schemas.character import CharacterResponse
from app.schemas.common import ResponseModel
from app.services.character_service import CharacterService
from app.repositories.character_repo import CharacterRepository

router = APIRouter()




router.post()
