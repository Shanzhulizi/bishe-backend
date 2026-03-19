from datetime import datetime, timezone

from app.core.logging import get_logger
from app.repositories.behavior_repo import BehaviorRepository
from app.repositories.character_repo import CharacterRepository
from app.services.behavior_service import BehaviorService

logger = get_logger(__name__)
from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List, Optional

from app.models.character import Character
from app.schemas.character import CharacterCreate, CharacterUpdate


class CharacterService:
    def __init__(self, db: Session):
        self.db = db
        self.character_repo = CharacterRepository(db)
        self.behavior_repo = BehaviorRepository(db)

    def get_characters(
            self,
            skip: int = 0,
            limit: int = 20,
            category_id: Optional[int] = None,
            tag_id: Optional[int] = None,
            keyword: Optional[str] = None,
            is_official: Optional[bool] = None
    ) -> tuple[List[Character], int]:
        """获取角色列表（支持筛选和搜索）"""

        characters, total = self.character_repo.get_all(skip, limit, category_id, tag_id, keyword, is_official)

        return characters, total

    def get_character(self, character_id: int) -> Optional[Character]:
        """获取单个角色详情"""
        return self.character_repo.get_by_id_with_relations(character_id)

    def create_character(self, data: CharacterCreate) -> Character:
        """创建角色"""

        # 不检查名称是否已经存在，允许重复名称，鼓励用户创作
        # existing = self.db.query(Character).filter(
        #     Character.name == data.name
        # ).first()
        # if existing:
        #     raise HTTPException(status_code=400, detail="角色名称已存在")

        # 创建角色
        character = self.character_repo.create_with_relations(data)
        return character

    def update_character(self, character_id: int, data: CharacterUpdate) -> Character:
        """更新角色"""

        # 2. 转换为字典
        update_data = data.dict(exclude_unset=True)

        # 3. 调用 repo 更新
        character = self.character_repo.update_complete(character_id, update_data)

        if not character:
            raise HTTPException(status_code=404, detail="角色不存在")

        # 4. 提交事务
        self.db.flush()

        return character

    def delete_character(self, character_id: int):
        """删除角色（软删除）"""
        is_deleted = self.character_repo.soft_delete(character_id)
        if not is_deleted:
            raise HTTPException(status_code=404, detail="删除错误")
        self.db.commit()

    def get_character_like_count(self, character_id) -> int:
        """获取角色的点赞数"""
        return self.character_repo.get_like_count(character_id)

    def get_character_chat_count(self, character_id) -> int:
        """获取角色的聊天数"""
        return self.behavior_repo.get_chats_count(character_id)

    def increment_like_count(self, character_id: int):
        """点赞角色"""
        logger.info(f"更新角色点赞数: character_id={character_id}")
        self.character_repo.increment_like_count(character_id)

    def decrement_like_count(self, character_id: int) -> bool:
        """
        取消点赞
        Returns:
            bool: 是否成功（False表示还没点赞）
        """
        logger.info(f"更新角色点赞数: character_id={character_id}")
        self.character_repo.decrement_like_count(character_id)
        return True

    def get_character_like_status(self, user_id, character_id):
        """获取用户对角色的点赞状态"""
        return self.behavior_repo.get_like_status(user_id, character_id)

    def batch_get_like_status(self, current_user, character_ids):
        """批量获取用户对多个角色的点赞状态"""
        # 查询当前用户对所有角色的点赞记录
        likes = self.behavior_repo.batch_get_like_status(current_user.id, character_ids)
        # 构建点赞状态映射
        liked_map = {like.character_id: True for like in likes}

        # 确保所有请求的 ID 都在返回结果中（未点赞的默认为 False）
        for char_id in character_ids:
            if char_id not in liked_map:
                liked_map[char_id] = False
        return liked_map

    def increment_view_count(self, character_id: int):
        """增加角色的浏览数（每次访问角色详情时调用）"""
        logger.info(f"更新角色点赞数: character_id={character_id}")
        self.character_repo.increment_view_count(character_id)

    def increment_chat_count(self, character_id):
        logger.info(f"更新角色聊天数: character_id={character_id}")
        self.character_repo.increment_chat_count(character_id)

    def update_use_time(self, character_id):
        logger.info(f"更新角色使用时间: character_id={character_id}")
        updated = CharacterUpdate(last_used_at=datetime.now(timezone.utc))
        self.update_character(character_id, updated)
