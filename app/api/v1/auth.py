from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from datetime import timedelta

from app.core.constants import ResponseCode
from app.db.session import get_db
from app.schemas.common import ResponseModel
from app.schemas.user import UserCreate, UserOut
from app.services.user_service import create_user
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.post("/register",   response_model=ResponseModel[UserOut])
def register(
        user_in: UserCreate,
       db:  AsyncSession = Depends(get_db),
):
    logger.info(f"注册用户: {user_in.username}")
    try:
        user = create_user(db, user_in)
        logger.info(f"用户注册成功,用户id: {user.id}")
        return ResponseModel.success(
            msg="注册成功",
            data=user,
        )
    except ValueError as e:

        return ResponseModel.error(
            code=ResponseCode.USER_ALREADY_EXISTS,
            msg="注册失败，" + str(e) + ""
        )
