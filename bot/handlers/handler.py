import io
from telegram import Update
from telegram.ext import CallbackContext
import os
import json
import bot.utils.module as md
import time
try:
    from config import max_context_limit
except ImportError as e:
    # 如果不想程序因配置错误而停止，可以设置默认值
    max_context_limit = 20  # 默认值
    # 或者，如果你想让程序因为缺少配置而停止，可以取消下面的注释
    # raise ImportError("Could not import settings from config.py") from e


def save_media(media, media_type, user_id):
    user_media_dir = f'media/{user_id}'
    if not os.path.exists(user_media_dir):
        os.makedirs(user_media_dir)

    # 为文件生成唯一的名称
    file_name = f'{media_type}_{int(time.time())}.ogg'
    file_path = os.path.join(user_media_dir, file_name)

    media.download(file_path)

    return file_path


def save_content(media_content, media_type, user_id):
    # 创建保存文件的目录
    user_media_dir = f'media/{user_id}'
    if not os.path.exists(user_media_dir):
        os.makedirs(user_media_dir)

    # 为文件生成唯一的名称
    file_name = f'{media_type}_{int(time.time())}.ogg'
    file_path = os.path.join(user_media_dir, file_name)

    # 写入文件
    with open(file_path, 'wb') as media_file:
        media_file.write(media_content.content)
    return file_path


class UserSession:
    def __init__(self, user_id):
        self.user_id = user_id
        self.messages = []
        self.context = ""
        user_media_dir = f'context/{user_id}'
        if not os.path.exists(user_media_dir):
            os.makedirs(user_media_dir)
        file_path = os.path.join(user_media_dir, f"context_{self.user_id}.json")
        self.context_file = f"{file_path}"
        self.load_context()

    def add_user_message(self, text):
        # 用户消息以 {"role": "user", "content": text} 的形式添加
        self.context.append({"role": "user", "content": text})
        self.trim_context()  # 确保上下文不会无限增长
        self.save_context()

    def add_system_message(self, text):
        # 系统消息以 {"role": "system", "content": text} 的形式添加
        self.context.append({"role": "system", "content": text})
        self.trim_context()  # 确保上下文不会无限增长
        self.save_context()

    def trim_context(self):
        # 如果需要，可以在这里限制上下文的大小
        max_context_length = max_context_limit
        self.context = self.context[-max_context_length:]

    def save_context(self):
        # 将上下文保存到文件
        with open(self.context_file, 'w') as file:
            json.dump(self.context, file, indent=4)

    def load_context(self):
        # 从文件加载上下文
        if os.path.exists(self.context_file):
            with open(self.context_file, 'r') as file:
                self.context = json.load(file)
        else:
            self.context = []

    def clear_context(self):
        # 清除上下文
        self.context = []
        if os.path.exists(self.context_file):
            os.remove(self.context_file)

    def get_formatted_context(self):
        # 获取格式化的上下文
        return self.context


user_sessions = {}


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('你好。')


def clear(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id not in user_sessions:
        user_sessions[user_id] = UserSession(user_id)
    user_sessions[user_id].clear_context()
    update.message.reply_text('上下文已清除')


def handle_text(update: Update, context) -> None:
    user_id = update.message.from_user.id
    user_message = update.message.text
    if user_id not in user_sessions:
        user_sessions[user_id] = UserSession(user_id)
    user_sessions[user_id].add_user_message(user_message)
    user_sessions[user_id].save_context()
    gpt_response = md.chat_with_gpt(user_message, user_id)
    user_sessions[user_id].add_system_message(gpt_response)
    user_sessions[user_id].save_context()
    gpt_whisper = md.tts_with_gpt(gpt_response)
    # temp_buffer = io.BytesIO()
    # gpt_whisper.stream_to_file(temp_buffer)
    answer_file_path = save_content(gpt_whisper, "ogg", user_id)
    # 发送语音回复
    with open(answer_file_path, 'rb') as answer:
        update.message.reply_voice(voice=answer)


def handle_voice(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id not in user_sessions:
        user_sessions[user_id] = UserSession(user_id)
    file = context.bot.getFile(update.message.voice.file_id)
    # 下载文件
    voice_file_path = save_media(file, "ogg", user_id)
    # 实现转换和处理流程（这里省略了错误处理和具体实现）
    transcribed_text = md.transcribe_audio_to_text(voice_file_path)
    user_sessions[user_id].add_user_message(transcribed_text)
    user_sessions[user_id].save_context()
    gpt_response = md.chat_with_gpt(transcribed_text, user_id)
    user_sessions[user_id].add_system_message(gpt_response)
    # temp_buffer = io.BytesIO()
    gpt_whisper = md.tts_with_gpt(gpt_response)
    user_sessions[user_id].save_context()
    # gpt_whisper.stream_to_file(temp_buffer)
    answer_file_path = save_content(gpt_whisper, "ogg", user_id)
    # 发送语音回复
    with open(answer_file_path, 'rb') as answer:
        update.message.reply_voice(voice=answer)
