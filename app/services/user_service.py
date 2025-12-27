from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import get_hash_password
from app.models.user import User
from app.core.logging import get_logger

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
