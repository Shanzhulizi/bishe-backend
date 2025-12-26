from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import auth,characters, chat
from app.models import character, message, conversation
from fastapi import FastAPI
from sqlalchemy import text

import uvicorn
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
from app.db.session import engine, Base, get_db
from app.models import  character  # 导入模型
# 创建所有表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI角色扮演聊天平台",
    description="基于FastAPI和Vue3的AI角色扮演聊天网站",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
# app.include_router(users.router, prefix="/api/users", tags=["用户"])
app.include_router(characters.router, prefix="/api/characters", tags=["角色"])
app.include_router(chat.router, prefix="/api/chat", tags=["聊天"])

@app.get("/")
async def root():
    return {"message": "AI角色扮演聊天平台API"}


@app.get("/health")
async def health_check(db=Depends(get_db)):
    # 测试数据库连接
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "db": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "db": "disconnected", "error": str(e)}


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )