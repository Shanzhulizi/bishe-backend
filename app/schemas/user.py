from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    """用户基础信息"""
    username: str
    email: EmailStr


class UserCreate(UserBase):
    """用户注册请求"""
    password: str


class UserLogin(BaseModel):
    """用户登录请求"""
    username: str
    password: str


class UserResponse(UserBase):
    """用户信息响应"""
    id: int
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    is_active: bool

    class Config:
        from_attributes = True  # 允许从ORM对象转换


class Token(BaseModel):
    """Token响应"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenData(BaseModel):
    """Token中的数据"""
    username: Optional[str] = None