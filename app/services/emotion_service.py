import asyncio
import json
from typing import Dict

import aiohttp
from types import SimpleNamespace
import ollama
import re
from app.core.config import Settings
from app.core.logging import get_logger
from types import SimpleNamespace

import ollama

from app.core.logging import get_logger

logger = get_logger(__name__)

settings = Settings()


class EmotionService:
    """情感分析服务"""

    def __init__(self):
        self.api_key = settings.DEEPSEEK_API_KEY
        self.api_url = settings.DEEPSEEK_BASE_URL



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



    async def analyze_use_model(self,message: str) -> dict:
        """
        使用本地 Ollama 模型分析情感

        返回格式:
        {
            "emotion": "开心",
            "score": 0.85,
            "raw_response": "情绪：开心，分数：0.85"
        }
        """
        try:
            # 构建消息 - 分开 system 和 user
            ollama_messages = [
                {
                    "role": "system",
                    "content": "你是一个情感分析专家。请分析用户消息中的情绪，从[开心,悲伤,愤怒,恐惧,惊讶,疑惑,厌恶,平静]中选择最符合的一个，并给出可信度分数（0-1之间的小数）。\n\n输出格式：情绪：xxx，分数：0.xx\n只输出这个格式，不要有其他内容。"
                },
                {
                    "role": "user",
                    "content": message
                }
            ]

            logger.info(f"发送到Ollama的消息: {ollama_messages}")

            # 调用 Ollama
            resp = ollama.chat(
                model="qwen2.5:7b",
                messages=ollama_messages,
                stream=False,
                options={
                    "temperature": 0.3,  # 降低温度，让输出更稳定
                    "num_predict": 100,  # 只需要很短的回复
                    "top_k": 40,
                    "top_p": 0.9,
                    "repeat_penalty": 1.1
                }
            )

            logger.info(f"Ollama原始回复: {resp}")

            # 提取回复内容
            if isinstance(resp, dict):
                if "message" in resp:
                    reply = resp["message"].get("content", "")
                elif "response" in resp:
                    reply = resp["response"]
                else:
                    reply = str(resp)
            else:
                reply = str(resp)

            logger.info(f"Ollama回复内容: {reply}")

            # 解析情绪和分数
            emotion, score = self.parse_emotion_response(reply)
            # 根据情绪映射到建议的回应语气
            tone = self._map_emotion_to_tone(emotion)

            # 返回字典格式
            return {
                "emotion": emotion,
                "score": score,
                "tone": tone,
                "raw_response": reply
            }

        except ollama.ResponseError as e:
            logger.error(f"Ollama响应错误: {e.error}")
            if "models not found" in str(e).lower():
                raise Exception(f"模型 'qwen2.5' 未安装，请运行: ollama pull qwen2.5")
            raise Exception(f"Ollama调用失败: {str(e)}")

        except Exception as e:
            logger.error(f"本地模型调用失败: {str(e)}")
            raise Exception(f"本地模型调用失败: {str(e)}")

    def _map_emotion_to_tone(self, emotion: str) -> str:
        """将情绪映射到建议的回应语气"""
        tone_map = {
            "开心": "活泼欢快",
            "悲伤": "温柔安慰",
            "愤怒": "冷静安抚",
            "恐惧": "温和鼓励",
            "惊讶": "热情回应",
            "疑惑": "耐心解释",
            "厌恶": "保持距离",
            "平静": "自然对话"
        }
        return tone_map.get(emotion, "自然对话")


    def parse_emotion_response(self,reply: str) -> tuple:
        """
        解析 Ollama 返回的情绪和分数

        支持格式:
        - "情绪：开心，分数：0.85"
        - "情绪：悲伤，分数：0.92"
        - "开心 0.85"
        - "开心 (0.85)"
        """
        emotions = ['开心', '悲伤', '愤怒', '恐惧', '惊讶', '疑惑', '厌恶', '平静']

        # 默认值
        emotion = "平静"
        score = 0.5

        try:
            # 方式1：匹配 "情绪：xxx，分数：0.xx"
            pattern1 = r'情绪[：:]\s*([\u4e00-\u9fa5]+)[，,]\s*分数[：:]\s*([0-9.]+)'
            match = re.search(pattern1, reply)

            if match:
                emotion = match.group(1)
                score = float(match.group(2))
                # 验证情绪是否在列表中
                if emotion not in emotions:
                    # 模糊匹配
                    for e in emotions:
                        if e in emotion:
                            emotion = e
                            break
                # 限制分数范围
                score = max(0.0, min(1.0, score))
                return emotion, score

            # 方式2：匹配 "开心 0.85" 或 "开心 (0.85)"
            pattern2 = r'([\u4e00-\u9fa5]+)\s*[（(]?([0-9.]+)[）)]?'
            match = re.search(pattern2, reply)

            if match:
                emotion = match.group(1)
                score = float(match.group(2))
                if emotion not in emotions:
                    for e in emotions:
                        if e in emotion:
                            emotion = e
                            break
                score = max(0.0, min(1.0, score))
                return emotion, score

            # 方式3：尝试在回复中找情绪词
            for e in emotions:
                if e in reply:
                    emotion = e
                    # 尝试找附近的数字作为分数
                    numbers = re.findall(r'0\.\d+|\d+\.\d+', reply)
                    if numbers:
                        score = float(numbers[0])
                        score = max(0.0, min(1.0, score))
                    break

            logger.warning(f"无法解析回复: {reply}，使用默认值")
            return emotion, score

        except Exception as e:
            logger.error(f"解析情绪失败: {e}, 回复: {reply}")
            return "平静", 0.5







# 创建全局实例
emotion_service = EmotionService()
