from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

from app.core.constants import ResponseCode

T = TypeVar('T')

class ResponseModel(BaseModel, Generic[T]):
    code: int
    msg: str
    data: Optional[T] = None

    @classmethod
    def success(cls, data: T = None, msg: str = "响应成功"):
        return cls(
            code=ResponseCode.SUCCESS,
            msg=msg,
            data=data
        )

    @classmethod
    def error(cls, code: ResponseCode, msg: str):
        return cls(
            code=code,
            msg=msg,
            data=None
        )