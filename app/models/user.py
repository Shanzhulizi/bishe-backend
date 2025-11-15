from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime
from sqlalchemy.sql import func
from app.database.session import Base


class User(Base):
    """用户表：存储平台用户信息"""
    __tablename__ = "users"  # 数据库中的表名

    # 主键
    id = Column(Integer, primary_key=True, index=True)

    # 用户身份信息
    username = Column(String(50), unique=True, index=True, nullable=False)  # 用户名，唯一且必须
    email = Column(String(100), unique=True, index=True, nullable=False)  # 邮箱，唯一且必须
    hashed_password = Column(String(255), nullable=False)  # 加密后的密码

    # 用户资料信息
    avatar_url = Column(String(500))  # 头像图片链接
    bio = Column(Text)  # 个人简介

    # 账户状态
    is_active = Column(Boolean, default=True)  # 账户是否激活

    # 时间戳
    created_at = Column(DateTime, default=func.now())  # 创建时间
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # 更新时间（自动更新）
