
import logging
import os

from TTS.api import TTS

from app.core.config import settings

logger = logging.getLogger(__name__)


class XTTSService:
    """XTTS 服务 - 完全模仿测试代码"""

    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._model is None:
            # 设置环境变量
            os.environ['TTS_HOME'] = str(settings.XTTS_MODEL_DIR)
            os.environ['TORCH_HOME'] = str(settings.XTTS_MODEL_DIR.parent)
            self._load_model()

    def _load_model(self):
        """加载 XTTS 模型 - 和测试代码完全一样"""
        try:
            logger.info("正在加载 XTTS 模型...")
            # 直接加载，不加多余参数
            self._model = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
            logger.info("✅ XTTS 模型加载成功")
        except Exception as e:
            logger.error(f"XTTS 模型加载失败: {e}")
            raise e

    def tts_to_file(self, text, speaker_wav, output_path, language="zh"):
        """
        直接调用模型的 tts_to_file - 和测试代码完全一样
        """
        try:

            logger.info(f"生成语音: {text[:20]}...")
            logger.info(f"使用 speaker_wav: {speaker_wav}")
            # 确保输出目录存在
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # 直接调用，不加任何包装
            self._model.tts_to_file(
                text=text,
                file_path=output_path,
                speaker_wav=speaker_wav,
                language=language,
                speed=1.0,  # 可以调整这个参数来控制语速
                temperature=0.9  # 可以调整这个参数来控制声音的多样性
            )

            logger.info(f"语音已生成: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"生成语音失败: {e}")
            raise e


# 全局实例
xtts_service = XTTSService()