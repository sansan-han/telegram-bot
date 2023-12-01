from openai import OpenAI
from pathlib import Path
import os
import json
try:
    from config import base_url, model, voice, role
except ImportError as e:
    # 如果不想程序因配置错误而停止，可以设置默认值
    base_url = "https://api.openai.com/v1"
    model = "gpt-3.5-turbo"
    voice = "onyx"
    role = "you are a helpful assistant!"
    # 或者，如果你想让程序因为缺少配置而停止，可以取消下面的注释
    # raise ImportError("Could not import settings from config.py") from e
try:
    from config import api_key
except ImportError as e:
    raise ImportError("INVALID API_KEY") from e

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)


# openai Whisper
def transcribe_audio_to_text(path):
    audio_file_path = Path(path)
    with audio_file_path.open('rb') as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
    return transcript


# GPT talk
def chat_with_gpt(text, user_id):
    user_media_dir = f'context/{user_id}'
    if not os.path.exists(user_media_dir):
        os.makedirs(user_media_dir)
    file_path = os.path.join(user_media_dir, f"context_{user_id}.json")
    context_file = f"{file_path}"
    if os.path.exists(context_file):
        with open(context_file, 'r') as file:
            messages_context = json.load(file)
    else:
        messages_context = [{"role": "system", "content": role}, {"role": "user", "content": text}]

    response = client.chat.completions.create(
        model=model,
        messages=messages_context
    )
    return response.choices[0].message.content


# TTS of openai
def tts_with_gpt(text):
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text
    )
    return response
