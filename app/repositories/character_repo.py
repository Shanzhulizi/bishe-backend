from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.models.character import Character
from app.models.character_configs import CharacterConfigs
from app.schemas.character import CharacterCreate


class CharacterRepository:

    def create_character(self, db: Session, data: CharacterCreate):
        # 创建角色基本信息
        char = Character(
            name=data.name,
            description=data.description,
            worldview=data.worldview,
            speech_style=data.speech_style,
        )
        db.add(char)
        db.flush()  # 获取 char.id

        # 创建角色配置
        config = CharacterConfigs(
            character_id=char.id,
            persona=data.persona or {}
        )
        db.add(config)

        db.commit()
        db.refresh(char)
        return char
