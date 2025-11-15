from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password


class UserService:
    @staticmethod
    def get_user_by_username(db: Session, username: str):
        """根据用户名获取用户"""
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str):
        """根据邮箱获取用户"""
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def create_user(db: Session, user: UserCreate):
        """创建新用户"""
        # 检查用户名是否已存在
        if UserService.get_user_by_username(db, user.username):
            return None, "用户名已存在"

        # 检查邮箱是否已存在
        if UserService.get_user_by_email(db, user.email):
            return None, "邮箱已被注册"

        # 创建用户
        hashed_password = get_password_hash(user.password)
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user, "注册成功"

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str):
        """验证用户"""
        user = UserService.get_user_by_username(db, username)
        if not user:
            return None, "用户不存在"
        if not verify_password(password, user.hashed_password):
            return None, "密码错误"
        if not user.is_active:
            return None, "账户已被禁用"
        return user, "登录成功"


user_service = UserService()