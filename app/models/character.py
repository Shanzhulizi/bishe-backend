from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.session import Base


class Character(Base):
    """AI角色表：存储所有可聊天的AI角色信息"""
    __tablename__ = "characters"

    # 主键
    id = Column(Integer, primary_key=True, index=True)

    # 角色基本信息
    name = Column(String(100), nullable=False, index=True)  # 角色名称
    description = Column(Text)  # 角色描述
    personality = Column(Text, nullable=False)  # 角色性格设定
    background = Column(Text)  # 角色背景故事

    # 对话相关
    greeting_message = Column(Text, nullable=False)  # 初次见面的问候语
    example_dialogue = Column(Text)  # 示例对话（用于训练AI）
    initial_prompt = Column(Text, nullable=False)  # 给AI的系统提示词（核心设定）

    # 展示信息
    avatar_url = Column(String(500))  # 角色头像链接
    tags = Column(JSON)  # 标签列表，如：["历史", "幽默", "导师"]

    # 权限和归属
    is_public = Column(Boolean, default=True)  # 是否公开可见
    created_by = Column(Integer, ForeignKey("users.id"))  # 创建者ID（外键）

    # 统计信息
    usage_count = Column(Integer, default=0)  # 被使用次数
    rating = Column(Integer, default=0)  # 平均评分（1-5分）

    # 时间戳
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # 关系定义（不是数据库字段，是SQLAlchemy的关系映射）
    creator = relationship("User")  # 关联到User模型，方便查询创建者信息

