from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.models.character import Character
from app.models.character_configs import CharacterConfigs
from app.schemas.character import CharacterCreate
from app.persona.builder import PersonaBuilder


class CharacterRepository:

    def create_character(self, db: Session,

                         *,
                         name: str,
                         avatar: Optional[str],
                         description: Optional[str],
                         worldview: Optional[str],
                         persona: dict
                         ):
        # 创建角色基本信息
        char = Character(
            name=name,
            avatar=avatar,
            description=description,
            worldview=worldview
        )
        db.add(char)
        db.flush()  # 拿到 char.id

        # 创建角色配置
        config = CharacterConfigs(
            character_id=char.id,
            persona=persona
        )
        db.add(config)

        db.commit()
        db.refresh(char)
        return char
