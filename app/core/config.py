from pydantic_settings import BaseSettings
from typing import List
from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    # API配置
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "AI角色扮演聊天平台"

    # 数据库配置
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    # CORS配置
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",  # Vite默认端口
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173"
    ]

    # 数据库配置
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    # JWT配置
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7天



    # DeepSeek配置

    # api_key = os.getenv("DEEPSEEK_API_KEY")
    DEEPSEEK_API_KEY: str

    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com/v1"
    DEEPSEEK_MODEL: str = "deepseek-chat"  # 或者 "deepseek-reasoner"


    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
