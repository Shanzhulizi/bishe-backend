from sqlalchemy import Column, Integer, Text, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.session import Base


class Message(Base):
    """消息表：存储每条聊天消息"""
    __tablename__ = "messages"

    # 主键
    id = Column(Integer, primary_key=True, index=True)

    # 消息归属
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)  # 所属会话ID

    # 消息内容
    role = Column(String(20), nullable=False)  # 发送者角色：'user'（用户）或 'assistant'（AI）
    content = Column(Text, nullable=False)  # 消息正文内容

    # 技术统计
    tokens_used = Column(Integer, default=0)  # 本条消息消耗的AI token数量（用于计费统计）

    # 消息状态
    is_archived = Column(Boolean, default=False)  # 是否已归档

    # 时间戳
    created_at = Column(DateTime, default=func.now())  # 消息发送时间

    # 关系定义
    conversation = relationship("Conversation", back_populates="messages")  # 关联到所属会话