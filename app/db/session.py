# 替换异步引擎为同步引擎
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

print(settings.DATABASE_URL)
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=30,
    pool_timeout=60,  # 获取连接的超时时间，从30秒适当调长
    pool_recycle=3600  # 建议设置，防止连接被数据库服务端断开
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
