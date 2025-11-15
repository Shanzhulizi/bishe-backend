from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.session import Base


class Conversation(Base):
    """对话会话表：每次聊天都是一个会话"""
    __tablename__ = "conversations"

    # 主键
    id = Column(Integer, primary_key=True, index=True)

    # 会话参与方
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # 用户ID（外键）
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=False)  # 角色ID（外键）

    # 会话信息
    title = Column(String(200), nullable=False)  # 会话标题（自动生成，如"与历史学者的对话"）
    message_count = Column(Integer, default=0)  # 当前会话中的消息总数
    last_message_at = Column(DateTime, default=func.now())  # 最后一条消息的时间

    # 会话状态
    is_archived = Column(Boolean, default=False)  # 是否已归档（相当于放到回收站）

    # 时间戳
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # 关系定义
    user = relationship("User")  # 关联用户
    character = relationship("Character")  # 关联角色
    messages = relationship(
        "Message",
        back_populates="conversation",  # 在Message模型中定义反向关联
        cascade="all, delete-orphan"  # 级联删除：删除会话时自动删除所有消息
    )



