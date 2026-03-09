# # app/services/cosyvoice_service.py
#
# import os
# import sys
# import uuid
# import torch
# import logging
# import soundfile as sf
# from pathlib import Path
# from typing import Optional, Dict
#
# import os
# import sys
# import torch
# import soundfile as sf
#
# # 添加 CosyVoice 路径
# # COSYVOICE_PATH = r"E:\Code\Python\AIChat\CosyVoice"
# from app.core.config import settings
#
# cosyvice_path = settings().COSYVOICE_PATH
# if cosyvice_path not in sys.path:
#     sys.path.insert(0, cosyvice_path)
#     print(f"✅ 添加路径: {cosyvice_path}")
#
# # 导入 CosyVoice
# try:
#     from CosyVoice.cosyvoice.cli.cosyvoice import CosyVoice
#
#     from CosyVoice.cosyvoice.utils.file_utils import load_wav
#
#     print("✅ CosyVoice 导入成功！")
# except ImportError as e:
#     print(f"❌ 导入失败: {e}")
#     print("请确保 CosyVoice 路径正确")
#     sys.exit(1)
#
# logger = logging.getLogger(__name__)
#
#
# class CosyVoiceService:
#     """CosyVoice 声音克隆服务"""
#
#     def __init__(self, model_path: str, output_dir: str = "outputs"):
#         """
#         初始化语音服务
#
#         Args:
#             model_path: CosyVoice 模型路径
#             output_dir: 音频输出目录
#         """
#         self.model_path = Path(model_path)
#         self.output_dir = Path(output_dir)
#         self.output_dir.mkdir(parents=True, exist_ok=True)
#
#         # 角色声音缓存 {role_id: {"text": 参考文本, "audio": 音频路径}}
#         self.role_voices: Dict[str, dict] = {}
#
#         # 加载模型
#         self._load_model()
#
#     def _load_model(self):
#         """加载 CosyVoice 模型"""
#         logger.info("📥 加载 CosyVoice 模型中...")
#         try:
#             self.model = CosyVoice(str(self.model_path))
#             logger.info("✅ 模型加载成功")
#
#             # 检查 CUDA
#             if torch.cuda.is_available():
#                 logger.info(f"   GPU: {torch.cuda.get_device_name(0)}")
#                 logger.info(f"   显存: {torch.cuda.get_device_properties(0).total_memory / 1024 ** 3:.1f}GB")
#         except Exception as e:
#             logger.error(f"❌ 模型加载失败: {e}")
#             raise
#
#     def generate(
#             self,
#             text: str,
#             prompt_text: str,
#             prompt_wav: str,
#             output_file: str
#     ):
#         """
#         生成语音
#         """
#
#         for output in self.model.inference_zero_shot(
#                 text,
#                 prompt_text,
#                 prompt_wav
#         ):
#
#             tts_speech = output["tts_speech"]
#
#             if torch.is_tensor(tts_speech):
#                 tts_speech = tts_speech.cpu().numpy()
#
#             if len(tts_speech.shape) > 1:
#                 tts_speech = tts_speech.squeeze()
#
#             sf.write(output_file, tts_speech, 22050)
#
#             return output_file
#
#
# # 全局实例
# cosyvoice_service = CosyVoiceService(settings.COSYVOICE_MODEL_DIR, settings.COSYVOICE_OUTPUT_DIR)
