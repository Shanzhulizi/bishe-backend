import asyncio
import platform

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import auth, characters, chat
from app.core.config import settings
from app.core.logging import setup_logging

if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())




# 启动日志
setup_logging()


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




if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        # reload=True,

        loop="asyncio"  # 关键参数
    )