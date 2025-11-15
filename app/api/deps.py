# from fastapi import Depends, HTTPException, status
# from fastapi.security import HTTPBearer
# from app.core.security import verify_token
# from app.schemas.user import TokenData
#
# security = HTTPBearer()
# async def get_current_user(token: str = Depends(security)):
#     """获取当前用户依赖"""
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#
#     payload = verify_token(token.credentials)
#     if payload is None:
#         raise credentials_exception
#
#     username: str = payload.get("sub")
#     if username is None:
#         raise credentials_exception
#
#     return TokenData(username=username)


from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from app.core.security import verify_token
from app.schemas.user import TokenData
from app.database.session import get_db
from app.models.user import User

security = HTTPBearer()


async def get_current_user(
        token: str = Depends(security),
        db: Session = Depends(get_db)
):
    """获取当前用户（返回完整的User对象）"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = verify_token(token.credentials)
    if payload is None:
        raise credentials_exception

    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception

    # 从数据库获取完整的用户信息
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception

    return user


# 可选：保留原来的只返回TokenData的版本
async def get_current_user_data(token: str = Depends(security)):
    """获取当前用户数据（只返回TokenData）"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = verify_token(token.credentials)
    if payload is None:
        raise credentials_exception

    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception

    return TokenData(username=username)