import asyncio
import json
from typing import Dict

import aiohttp

from app.core.config import Settings
from app.core.logging import get_logger

logger = get_logger(__name__)

settings = Settings()


class EmotionService:
    """情感分析服务"""

    def __init__(self):
        self.api_key = settings.DEEPSEEK_API_KEY
        self.api_url = settings.DEEPSEEK_BASE_URL



    async def analyze_use_model(self, text: str) -> dict:
        pass

    async def analyze_use_api(self, text: str) -> Dict:
        """使用 DeepSeek 分析文本情感"""

        # 如果没有配置 API key，返回默认值
        if not self.api_key:
            logger.warning("未配置 DeepSeek API Key，使用默认值")
            return self._default_response()

        # 构建提示词
        prompt = f"""分析下面文本的情感，只返回JSON格式，不要有其他文字：

                文本：{text}

                请分析出具体情感类别（如：开心、伤心、生气、惊讶、害怕、厌恶、喜爱、中性等），并给出置信度。

                返回格式：
                {{
                    "emotion": "情感类别",
                    "score": 0.0-1.0之间的置信度,
                    "reason": "简要分析原因",
                    "tone_suggestion": "根据这个情感，AI应该用什么样的语气回应"
                }}"""

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                        self.api_url,
                        headers={
                            "Authorization": f"Bearer {self.api_key}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": "deepseek-chat",
                            "messages": [
                                {"role": "system", "content": "你是一个情感分析专家，请严格按JSON格式返回。"},
                                {"role": "user", "content": prompt}
                            ],
                            "temperature": 0.1,  # 低温度，保证稳定性
                            "max_tokens": 200
                        },
                        timeout=10
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"DeepSeek API 错误: {response.status} - {error_text}")
                        return self._default_response()

                    result = await response.json()

                    # 解析返回的 JSON
                    content = result['choices'][0]['message']['content']

                    # 提取 JSON 部分（防止有额外文字）
                    json_start = content.find('{')
                    json_end = content.rfind('}') + 1
                    if json_start >= 0 and json_end > json_start:
                        content = content[json_start:json_end]

                    emotion_data = json.loads(content)

                    # 构建返回格式
                    emotion = emotion_data.get('emotion', '中性')
                    score = float(emotion_data.get('score', 0.8))

                    # 情感对应的语气建议（API 返回的优先，否则用默认）
                    tone_map = {
                        '开心': '用户很开心，用活泼愉快的语气回应',
                        '伤心': '用户很难过，用温柔安慰的语气回应',
                        '生气': '用户很生气，保持冷静耐心',
                        '惊讶': '用户很惊讶，用热情的语气回应',
                        '害怕': '用户有些害怕，用安心的语气回应',
                        '厌恶': '用户有些反感，用平和的语气回应',
                        '喜爱': '用户很喜欢，用亲切的语气回应',
                        '中性': '用平常的语气回应'
                    }

                    return {
                        'emotion': emotion,
                        'score': score,
                        'tone': emotion_data.get('tone_suggestion', tone_map.get(emotion, '用平常的语气回应')),
                        'reason': emotion_data.get('reason', ''),
                        'needs_comfort': emotion in ['伤心', '害怕'],
                        'needs_calm': emotion == '生气'
                    }

        except asyncio.TimeoutError:
            logger.error("DeepSeek API 超时")
            return self._default_response()
        except Exception as e:
            logger.error(f"DeepSeek 情感分析失败: {e}")
            return self._default_response()

    def _default_response(self):
        """默认返回"""
        return {
            'emotion': '中性',
            'score': 0.5,
            'tone': '用平常的语气回应',
            'reason': '',
            'needs_comfort': False,
            'needs_calm': False
        }


# 创建全局实例
emotion_service = EmotionService()
