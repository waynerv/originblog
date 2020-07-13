from typing import Optional

from fastapi.encoders import jsonable_encoder


class CustomError(Exception):
    status_code = None
    message = None

    def __init__(self, message: Optional[str] = None, status_code: Optional[int] = None,
                 detail: Optional[list] = None) -> None:
        super().__init__()
        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code

        self.detail = jsonable_encoder(detail) if detail else None

    def __str__(self) -> str:
        return self.message

    def to_dict(self) -> dict:
        rv = {
            'type': self.__class__.__name__,
            'message': self.message,
            'status': self.status_code,
            'detail': self.detail
        }
        return rv


class ValidationError(CustomError):
    status_code = 422
    message = '数据不合法'


class AuthorizeError(CustomError):
    status_code = 401
    message = '身份未认证'


class ForbiddenError(CustomError):
    status_code = 403
    message = '无操作权限'


class NotFoundError(CustomError):
    status_code = 404
    message = '资源不存在'


class InternalError(CustomError):
    status_code = 500
    message = '服务器内部错误'


class WechatError(CustomError):
    status_code = 500
    message = '企业微信API请求失败'
