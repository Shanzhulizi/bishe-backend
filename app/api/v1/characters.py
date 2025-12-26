from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.models.character import Character
from app.models.user import User
from app.schemas.character import CharacterCreate, CharacterResponse
from app.api.deps import get_current_user

router = APIRouter()

