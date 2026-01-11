import logging
from typing import List
import httpx
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.constants import ResponseCode
from app.db.session import get_db
from app.repositories.character_repo import CharacterRepository
from app.schemas.chat import ChatRequest, ChatResponse
from app.schemas.common import ResponseModel
from app.services.character_service import CharacterService

router = APIRouter()
service = CharacterService(CharacterRepository())


async def call_deepseek_api(messages: List[dict]) -> ChatResponse:
    """
    调用DeepSeek API

    Args:
        messages: 消息列表，格式如 [{"role": "system", "content": "..."}, ...]

    Returns:
        ChatResponse: 包含回复和使用信息
    """
    api_url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": settings.DEEPSEEK_MODEL,  # 例如 "deepseek-chat"
        "messages": messages,
        "temperature": 0.7,  # 可调整
        "max_tokens": 2000,  # 根据角色设置调整
        "stream": False  # 如果需要流式响应改为True
    }

    # 添加可选的参数
    if hasattr(settings, 'DEEPSEEK_FREQUENCY_PENALTY'):
        payload["frequency_penalty"] = settings.DEEPSEEK_FREQUENCY_PENALTY

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(api_url, json=payload, headers=headers)
            response.raise_for_status()

            data = response.json()

            # 解析响应
            if data.get("choices") and len(data["choices"]) > 0:
                reply = data["choices"][0]["message"]["content"]
                usage = data.get("usage", {})
                finish_reason = data["choices"][0].get("finish_reason")

                return ChatResponse(
                    reply=reply,
                    usage=usage,
                    finish_reason=finish_reason
                )
            else:
                raise Exception("API返回格式异常")

        except httpx.TimeoutException:
            raise Exception("API请求超时")
        except httpx.HTTPStatusError as e:
            error_msg = f"HTTP错误: {e.response.status_code}"
            try:
                error_detail = e.response.json()
                error_msg += f" - {error_detail.get('message', str(error_detail))}"
            except:
                pass
            raise Exception(error_msg)
        except Exception as e:
            raise Exception(f"API调用失败: {str(e)}")


# 3. 修改你的路由函数（改为异步）
@router.post("/send")
async def chat(
        req: ChatRequest,
        db: Session = Depends(get_db)
):
    # 1. 查询角色
    character = service.get_character_by_id(db, req.character_id)
    if not character:
        return ResponseModel.error(
            code=ResponseCode.NOT_FOUND,
            msg="角色不存在"
        )
    logging.info(f"获取req内容：{req}")
    # 2. 构造 system prompt（可以改进）
    system_prompt = build_system_prompt(character)

    # 3. 构造上下文（可以添加长度限制）
    messages = [{"role": "system", "content": system_prompt}]

    if req.history:
        # 限制历史记录长度，防止token超限
        max_history = getattr(settings, 'MAX_HISTORY_LENGTH', 10)
        recent_history = req.history[-max_history:] if len(req.history) > max_history else req.history

        messages.extend(
            {"role": m.role, "content": m.content}
            for m in recent_history
        )

    messages.append({
        "role": "user",
        "content": req.message
    })

    # 4. 调用实际的API
    try:
        chat_response = await call_deepseek_api(messages)

        # 5. 可选：保存对话历史到数据库
        # await save_conversation(db, req, character, chat_response)

        return ResponseModel.success(
            data={
                "reply": chat_response.reply,
                "usage": chat_response.usage,  # 返回使用量信息
                "finish_reason": chat_response.finish_reason
            }
        )

    except Exception as e:
        # 记录错误日志
        print(f"API调用错误: {str(e)}")

        return ResponseModel.error(
            code=ResponseCode.SERVICE_ERROR,
            msg=f"AI服务暂时不可用: {str(e)}"
        )


# 4. 改进的system prompt构建函数
def build_system_prompt(character):
    """构建更详细的角色扮演prompt"""
    prompt = f"""你正在扮演一个角色，请完全沉浸在这个角色中。

角色名称：{character.name}
角色设定：{character.description}

重要要求：
1. 请始终以{character.name}的身份思考和回应
2. 不要提及你是AI或助手
3. 保持角色设定的一致性
4. 对话风格要符合角色特点

现在开始角色扮演："""
    return prompt

# # 5. 可选：保存对话记录的函数
# async def save_conversation(db, req, character, chat_response):
#     """保存对话记录到数据库"""
#     try:
#         # 创建对话记录对象
#         conversation = Conversation(
#             character_id=req.character_id,
#             user_message=req.message,
#             ai_response=chat_response.reply,
#             tokens_used=chat_response.usage.get("total_tokens", 0) if chat_response.usage else 0,
#             # 可以添加更多字段
#         )
#         db.add(conversation)
#         db.commit()
#     except Exception as e:
#         db.rollback()
#         print(f"保存对话记录失败: {str(e)}")
