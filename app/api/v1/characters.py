from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.logging import get_logger
from app.repositories.character_repo import CharacterRepository
from app.schemas.character import CharacterCreate
from app.schemas.character import CharacterResponse
from app.schemas.common import ResponseModel
from app.services.character_service import CharacterService

router = APIRouter()
service = CharacterService(CharacterRepository())

logger = get_logger(__name__)


@router.post("/create", response_model=CharacterResponse)
def create_character(data: CharacterCreate, db: Session = Depends(get_db)):
    char = service.create_character(db, data)
    logger.info(f"创建角色成功: {char.id} - {char.name}")
    return {
        "id": char.id,
        "name": char.name,
        "avatar": char.avatar,
        "description": char.description,
        "worldview": char.worldview,
        "is_active": True,
        "persona": char.config.persona if char.config else {}
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
        data=[dict(id=c.id, name=c.name, avatar=c.avatar, description=c.description) for c in chars])


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
