import openai
from typing import List, Dict
import logging
from app.core.config import settings

# 配置日志
logger = logging.getLogger(__name__)


class LLMClient:
    def __init__(self):
        # # 配置OpenAI客户端
        # self.client = openai.OpenAI(
        #     api_key=settings.OPENAI_API_KEY,
        #     base_url=settings.OPENAI_BASE_URL
        # )
        # self.model = settings.OPENAI_MODEL

        # 配置DeepSeek客户端
        self.client = openai.OpenAI(
            api_key=settings.DEEPSEEK_API_KEY,
            base_url=settings.DEEPSEEK_BASE_URL
        )
        self.model = settings.DEEPSEEK_MODEL

    async def generate_response(self, messages: List[Dict]) -> str:
        """
        调用DeepSeek API生成回复
        """
        try:
            logger.info(f"调用DeepSeek API，模型: {self.model}")

            # 调用DeepSeek API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=2048,  # DeepSeek支持更长的回复
                top_p=0.9,
                frequency_penalty=0.1,
                presence_penalty=0.1,
                stream=False
            )

            # 提取回复内容
            reply = response.choices[0].message.content.strip()
            logger.info(f"DeepSeek回复成功，长度: {len(reply)}")

            return reply

        except openai.APIError as e:
            logger.error(f"DeepSeek API错误: {e}")
            return "抱歉，AI服务暂时不可用，请稍后重试。"

        except openai.APIConnectionError as e:
            logger.error(f"DeepSeek连接错误: {e}")
            return "网络连接出现问题，请检查网络后重试。"

        except openai.RateLimitError as e:
            logger.error(f"DeepSeek频率限制: {e}")
            return "请求过于频繁，请稍后重试。"

        except Exception as e:
            logger.error(f"DeepSeek未知错误: {e}")
            return "系统出现未知错误，请稍后重试。"

    # async def generate_response(self, messages: List[Dict]) -> str:
    #     """
    #     调用ChatGPT API生成回复
    #     """
    #     try:
    #         logger.info(f"调用ChatGPT API，模型: {self.model}")
    #
    #         # 调用OpenAI API
    #         response = self.client.chat.completions.create(
    #             model=self.model,
    #             messages=messages,
    #             temperature=0.7,  # 控制创造性，0-1之间
    #             max_tokens=1000,  # 最大回复长度
    #             top_p=0.9,  # 核采样参数
    #             frequency_penalty=0.1,  # 减少重复内容
    #             presence_penalty=0.1,  # 增加话题新鲜度
    #         )
    #
    #         # 提取回复内容
    #         reply = response.choices[0].message.content.strip()
    #         logger.info(f"ChatGPT回复成功，长度: {len(reply)}")
    #
    #         return reply
    #
    #     except openai.APIError as e:
    #         logger.error(f"OpenAI API错误: {e}")
    #         return "抱歉，AI服务暂时不可用，请稍后重试。"
    #
    #     except openai.APIConnectionError as e:
    #         logger.error(f"OpenAI连接错误: {e}")
    #         return "网络连接出现问题，请检查网络后重试。"
    #
    #     except openai.RateLimitError as e:
    #         logger.error(f"OpenAI频率限制: {e}")
    #         return "请求过于频繁，请稍后重试。"
    #
    #     except Exception as e:
    #         logger.error(f"未知错误: {e}")
    #         return "系统出现未知错误，请稍后重试。"