from http.client import HTTPException

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import ResponseCode
from app.core.security import get_hash_password, verify_password, create_access_token, decode_access_token
from app.exceptions import BizException
from app.models.user import User
from app.core.logging import get_logger
from app.repositories.user_repo import UserRepository
# app/api/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.db.session import get_db
from app.repositories.user_repo import UserRepository
logger = get_logger(__name__)


def create_user(db: AsyncSession, user_in) -> User:
    # 1. 检查用户名是否已存在
    result = db.execute(
        select(User).where(User.username == user_in.username)
    )

    if result.scalar_one_or_none():
        logger.waring(f"用户{user_in.username}已存在")
        raise ValueError("Username already exists")

    # 2. 查重（email）
    if user_in.email:
        result = db.execute(
            select(User).where(User.email == user_in.email)
        )
        if result.scalar_one_or_none():
            logger.waring(f"邮箱{user_in.email}已注册")
            raise ValueError("邮箱已存在")

    logger.info(f"准备创建用户: {user_in.username}")
    # 2. 构造用户对象
    user = User(
        username=user_in.username,
        email=user_in.email,
        password_hash=get_hash_password(user_in.password)
    )

    # 3. 添加到数据库
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception:
        db.rollback()
        raise

    logger.info(f"用户注册完成")
    return user


def user_login(db: AsyncSession, username: str, password: str) -> str:
    user = UserRepository.get_by_username(db, username)
    logger.info(f"用户登录服务 {user.username}")
    if not user:
        logger.warning(f"用户{username}不存在")
        raise BizException(ResponseCode.USER_NOT_FOUND)
    if not verify_password(password, user.password_hash):
        logger.warning(f"用户{username}密码错误")
        raise BizException(ResponseCode.PASSWORD_ERROR)
    if not user.is_active:
        logger.warning(f"用户{username}已停用")
        raise BizException(ResponseCode.USER_DISABLED)

    return create_access_token(username)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")



def get_current_user(token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
                     ) :
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED
        )
    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="token 缺少 username")
    user = UserRepository.get_by_username(db, username)

    if not user:
        raise HTTPException(status_code=401, detail="用户不存在")

    return user
