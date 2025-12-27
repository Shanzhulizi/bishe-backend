from pydantic import BaseModel, EmailStr, Field


# 注册请求 Schema
class UserCreate(BaseModel):
    username: str = Field(...,min_length=3,max_length=50)
    email: EmailStr | None= None
    password: str = Field(...,min_length=6,max_length=128)

# 注册成功返回 Schema
class UserOut(BaseModel):
    id: int
    username: str
    email : EmailStr | None
    is_active: bool

    class Config:
        from_attributes = True