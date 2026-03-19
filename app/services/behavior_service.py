# app/services/behavior_service.py
from datetime import datetime

from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.models.user_behavior import UserBehavior
from app.repositories.behavior_repo import BehaviorRepository

logger = get_logger(__name__)
class BehaviorService:
    def __init__(self, db: Session):
        self.db = db
        self.behavoir_repo = BehaviorRepository(db)

    def record_view(self, user_id: int, character_id: int):
        """记录浏览"""
        logger.info(f"记录浏览行为 - 用户ID: {user_id}, 角色ID: {character_id}")
        record = self.behavoir_repo.get_behavior(user_id, character_id, 'view')
        if not record:
            # 只有当天没有浏览记录才记录浏览行为，避免重复记录
            self.behavoir_repo .record_view(user_id, character_id)
            return True
        return False
    def record_chat(self, user_id: int, character_id: int):
        """记录聊天"""
        logger.info(f"记录聊天行为 - 用户ID: {user_id}, 角色ID: {character_id}")
        self.behavoir_repo .record_chat(user_id, character_id)

    def record_like(self, user_id: int, character_id: int):
        """记录点赞"""
        logger.info(f"记录点赞行为 - 用户ID: {user_id}, 角色ID: {character_id}")
        self.behavoir_repo. record_like(user_id, character_id)

    def delete_records(self, user_id: int, character_id: int, behavior_type: str):
        """删除用户行为记录"""
        logger.info(f"删除用户行为记录 - 用户ID: {user_id}, 角色ID: {character_id}, 行为类型: {behavior_type}")
        self.behavoir_repo.delete_records(user_id, character_id, behavior_type)

    def get_like_record(self,user_id: int, character_id: int):
        """获取用户点赞行为记录"""
        logger.info(f"获取用户行为记录 - 用户ID: {user_id}, 角色ID: {character_id}")
        return self.behavoir_repo.get_like_record(user_id, character_id)

