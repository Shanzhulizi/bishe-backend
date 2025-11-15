from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.api.deps import get_current_user
from app.database.session import get_db
from app.schemas.user import UserCreate, UserResponse, Token
from app.services.user_service import user_service
from app.core.security import create_access_token
from app.core.config import settings

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """用户注册"""
    user, message = user_service.create_user(db, user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
    return user


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """用户登录"""
    user, message = user_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message,
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 创建access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        user=user
    )


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """获取当前用户信息"""
    user = user_service.get_user_by_username(db, current_user.username)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user