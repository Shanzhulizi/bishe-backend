from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 创建数据库引擎（相当于Java的DataSource）
engine = create_engine(
    "sqlite:///./ai_chat.db",  # 数据库文件会在项目根目录创建
    connect_args={"check_same_thread": False}  # SQLite需要这个参数
)

# 创建数据库会话工厂（相当于Java的SessionFactory）
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类，所有模型都继承这个
Base = declarative_base()

# 依赖注入，在API路由中使用
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()