# app/services/cosyvoice_service.py

import os
import sys
import uuid
import torch
import logging
import soundfile as sf
from pathlib import Path
from typing import Optional, Dict

import os
import sys
import torch
import soundfile as sf

from app.core.config import Settings
from app.repositories import voice_repo
from app.repositories.voice_repo import VoiceRepository

settings = Settings()
cosyvice_path = settings.COSYVOICE_PATH
if cosyvice_path not in sys.path:
    sys.path.insert(0, str(cosyvice_path))
    print(f"✅ 添加路径: {cosyvice_path}")
# 导入 CosyVoice
try:
    from CosyVoice.cosyvoice.cli.cosyvoice import CosyVoice
    from CosyVoice.cosyvoice.utils.file_utils import load_wav

    print("✅ CosyVoice 导入成功！")
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    print("请确保 CosyVoice 路径正确")
    sys.exit(1)

logger = logging.getLogger(__name__)
voice_repo = VoiceRepository()


class CosyVoiceService:

    def __init__(self, model_path):
        self.model = CosyVoice(model_path)


    def generate(self, text, voice_id):

        # 检查 CUDA
        if torch.cuda.is_available():
            print(f"✅ GPU: {torch.cuda.get_device_name(0)}")
            print(f"   显存: {torch.cuda.get_device_properties(0).total_memory / 1024 ** 3:.1f} GB")

        voice = voice_repo.get_voice_by_id(voice_id)
        prompt_text = voice.voice_text
        BASE_DIR = Path(__file__).resolve().parent.parent.parent

        prompt_wav = str(BASE_DIR )+ voice.voice_url
        logger.info(f"路径信息: BASE_DIR={BASE_DIR} ,prompt_wav={prompt_wav}")

        # text=str(text)
        output_file_name = voice_id + uuid.uuid4().hex[:16] + ".wav"
        output_file = settings.COSYVOICE_OUTPUT_DIR / output_file_name
        # logger.info(f"生成语音: text={text}, voice_id={voice_id}, prompt_text={prompt_text}, prompt_wav={prompt_wav}, output_file={output_file}")

        try:
            # ✅ 正确：传入音频文件路径，而不是音频数据
            for i, output in enumerate(self.model.inference_zero_shot(
                    text,  # 要生成的文本
                    prompt_text,  # 参考音频的文本内容
                    prompt_wav  # 直接传入音频文件路径，不要用 load_wav！
            )):
                # output_file = "cloned_voice.wav"

                # 改为：
                tts_speech = output['tts_speech']
                if torch.is_tensor(tts_speech):
                    tts_speech = tts_speech.cpu().numpy()
                if len(tts_speech.shape) > 1:
                    tts_speech = tts_speech.squeeze()
                sf.write(output_file, tts_speech, 22050)

                # 获取音频信息
                audio_out, sr = sf.read(output_file)
                duration = len(audio_out) / sr

                print(f"\n✅ 克隆成功！")
                print(f"   - 输出文件: {output_file}")
                print(f"   - 音频时长: {duration:.2f}秒")
                print(f"   - 采样率: {sr}Hz")
                print(f"   - 文件大小: {os.path.getsize(output_file) / 1024:.1f}KB")

                # 可选：播放提示
                print(f"\n💡 可以用播放器打开: {os.path.abspath(output_file)}")

                audio_url = f"/static/cosyvoice/cosyvoice_output/{output_file_name}"

                return audio_url


        except Exception as e:
            print(f"❌ 克隆失败: {e}")
            import traceback

            traceback.print_exc()


cosyvoice_service = CosyVoiceService(model_path=settings.COSYVOICE_MODEL_DIR)
