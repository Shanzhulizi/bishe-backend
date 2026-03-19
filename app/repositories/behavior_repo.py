from datetime import datetime, date

from app.models.user_behavior import UserBehavior


class BehaviorRepository:
    def __init__(self, db):
        self.db = db

    def get_behavior(self, user_id: int, character_id: int, behavior_type: str):
        """获取用户行为"""
        # 获取今天的开始和结束时间
        today_start = datetime.combine(date.today(), datetime.min.time())  # 今天 00:00:00
        today_end = datetime.combine(date.today(), datetime.max.time())  # 今天 23:59:59.999999

        return self.db.query(UserBehavior).filter(
            UserBehavior.user_id == user_id,
            UserBehavior.character_id == character_id,
            UserBehavior.behavior_type == behavior_type,
            UserBehavior.created_at.between(today_start, today_end)
        ).first()

    def get_like_record(self, user_id: int, character_id: int):
        """获取点赞记录"""
        return self.db.query(UserBehavior).filter(
            UserBehavior.user_id == user_id,
            UserBehavior.character_id == character_id,
            UserBehavior.behavior_type == 'like'

        ).first()

    def record_view(self, user_id: int, character_id: int):
        """记录浏览"""
        behavior = UserBehavior(
            user_id=user_id,
            character_id=character_id,
            behavior_type='view',
            created_at=datetime.now()
        )
        self.db.add(behavior)


    def record_chat(self, user_id: int, character_id: int):
        """记录聊天"""
        behavior = UserBehavior(
            user_id=user_id,
            character_id=character_id,
            behavior_type='chat',
            created_at=datetime.now()
        )
        self.db.add(behavior)
        self.db.commit()

    def record_like(self, user_id: int, character_id: int):
        """记录点赞"""
        behavior = UserBehavior(
            user_id=user_id,
            character_id=character_id,
            behavior_type='like',
            created_at=datetime.now()
        )
        self.db.add(behavior)
        self.db.commit()

    def delete_records(self, user_id, character_id, behavior_type):
        self.db.query(UserBehavior).filter(
            UserBehavior.user_id == user_id,
            UserBehavior.character_id == character_id,
            UserBehavior.behavior_type == behavior_type
        ).delete()
        self.db.commit()

    def get_views_count(self, character_id: int):
        """获取浏览次数"""
        return self.db.query(UserBehavior).filter(
            UserBehavior.character_id == character_id,
            UserBehavior.behavior_type == 'view'
        ).count()
    def get_chats_count(self, character_id: int):
        """获取聊天次数"""
        return self.db.query(UserBehavior).filter(
            UserBehavior.character_id == character_id,
            UserBehavior.behavior_type == 'chat'
        ).count()
    def get_likes_count(self, character_id: int):
        """获取点赞次数"""
        return self.db.query(UserBehavior).filter(
            UserBehavior.character_id == character_id,
            UserBehavior.behavior_type == 'like'
        ).count()



    def get_like_status(self, id, character_id):
        """获取点赞状态"""
        is_liked = self.db.query(UserBehavior).filter(
            UserBehavior.character_id == character_id,
            UserBehavior.user_id == id,
            UserBehavior.behavior_type == 'like'
        ).first() is not None
        return is_liked

    def batch_get_like_status(self, id, character_ids):
        """批量获取点赞状态"""
        likes = self.db.query(UserBehavior).filter(
            UserBehavior.character_id.in_(character_ids),
            UserBehavior.user_id == id,
            UserBehavior.behavior_type == 'like'
        ).all()
        return likes