from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.models.character import Character
from app.models.user import User
from app.schemas.character import CharacterCreate, CharacterResponse
from app.api.deps import get_current_user

router = APIRouter()


@router.post("/", response_model=CharacterResponse)
async def create_character(
        character: CharacterCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """创建新角色"""
    # 检查角色名是否已存在（对于当前用户）
    existing_character = db.query(Character).filter(
        Character.name == character.name,
        Character.created_by == current_user.id
    ).first()

    if existing_character:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="您已创建过同名的角色"
        )

    # 创建角色
    db_character = Character(
        **character.dict(),
        created_by=current_user.id
    )

    db.add(db_character)
    db.commit()
    db.refresh(db_character)

    return db_character


@router.get("/", response_model=List[CharacterResponse])
async def get_characters(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """获取用户创建的角色列表"""
    characters = db.query(Character).filter(
        Character.created_by == current_user.id
    ).offset(skip).limit(limit).all()

    return characters


@router.get("/public", response_model=List[CharacterResponse])
async def get_public_characters(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    """获取公开角色列表"""
    characters = db.query(Character).filter(
        Character.is_public == True
    ).offset(skip).limit(limit).all()

    return characters


@router.get("/{character_id}", response_model=CharacterResponse)
async def get_character(
        character_id: int,
        db: Session = Depends(get_db)
):
    """获取角色详情"""
    character = db.query(Character).filter(Character.id == character_id).first()

    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="角色不存在"
        )

    if not character.is_public and character.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问此角色"
        )

    return character