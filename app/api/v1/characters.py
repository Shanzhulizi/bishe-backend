import shutil

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.core.logging import get_logger
from app.repositories.character_repo import CharacterRepository
from app.schemas.character import CharacterCreate
from app.schemas.character import CharacterResponse
from app.schemas.common import ResponseModel
from app.services.character_service import CharacterService
import os
import uuid
import json
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from pathlib import Path

router = APIRouter()
service = CharacterService(CharacterRepository())

logger = get_logger(__name__)

# 确保头像目录存在
AVATAR_DIR = Path("static/avatars")
AVATAR_DIR.mkdir(parents=True, exist_ok=True)


# @router.post("/create", response_model=CharacterResponse)
# def create_character(data: CharacterCreate, db: Session = Depends(get_db)):
#     char = service.create_character(db, data)
#     logger.info(f"创建角色成功: {char.id} - {char.name}")
#     return {
#         "id": char.id,
#         "name": char.name,
#         "avatar": char.avatar,
#         "description": char.description,
#         "worldview": char.worldview,
#         "is_active": True,
#         "persona": char.config.persona if char.config else {}
#     }


@router.post("/create", response_model=CharacterResponse)
def create_character(
        name: str = Form(...),
        description: str = Form(None),
        worldview: str = Form(None),
        tags: str = Form(""),
        avatar: UploadFile = File(None),
        db: Session = Depends(get_db),
):
    logger.info(f"name:{name}")
    logger.info(f"description:{description}")
    logger.info(f"worldview:{worldview}")
    logger.info(f"tags:{tags}")
    logger.info(f"avatar:{avatar}")
    avatar_url = None
    logger.info("test")
    if avatar:
        ext = avatar.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        file_path = AVATAR_DIR / filename

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(avatar.file, buffer)

        avatar_url = f"http://localhost:8000/static/avatars/{filename}"

    logger.info("test")
    tag_list = tags.split(",") if tags else []

    data = CharacterCreate(
        name=name,
        avatar=avatar_url,
        description=description,
        worldview=worldview,
        tags=tag_list,
    )

    char = service.create_character(db, data)

    return {
        "id": char.id,
        "name": char.name,
        "avatar": char.avatar,
        "description": char.description,
        "worldview": char.worldview,
        "is_active": True,
        "persona": char.config.persona if char.config else {},
    }


@router.get("/list")
def list_characters(db: Session = Depends(get_db)):
    """
    获取所有角色的基本信息
    """
    chars = service.get_all_characters_basic(db)
    logger.info(f"获取所有角色基本信息成功，数量：{len(chars)}")
    # 返回统一格式
    return ResponseModel.success(
        data=[dict(id=c.id, name=c.name, avatar=c.avatar, description=c.description, like_count=c.like_count) for c in
              chars])


"""
/api/characters/list 被 误匹配到了 /api/characters/{id} 这个接口上
所以，id这个接口放到了最后
"""


@router.get("/{character_id}", response_model=CharacterResponse)
def get_character_by_id(character_id: int, db: Session = Depends(get_db)):
    logger.info(f"获取角色基本信息{character_id}")
    char = service.get_character_by_id(db, character_id)
    logger.info(f"获取角色基本信息成功：{char.id} - {char.name}")
    if not char:
        return None
    return {
        "id": char.id,
        "name": char.name,
        "avatar": char.avatar,
        "description": char.description,
    }
