from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from config import TOKEN, REQUEST_KWARGS
from telegram.utils.request import Request
from pathlib import Path
import handlers.handler as hd
import os
from datetime import datetime

# 定义存储路径
voice_folder = Path(__file__).parent / "voice"
answer_folder = Path(__file__).parent / "answer"

# 创建文件夹如果它们不存在
os.makedirs(voice_folder, exist_ok=True)
os.makedirs(answer_folder, exist_ok=True)

# 生成基于当前时间戳的文件名
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
voice_file_name = f"{timestamp}.ogg"
answer_file_name = f"{timestamp}.ogg"
voice_file_path = voice_folder / voice_file_name
answer_file_path = answer_folder / answer_file_name
# 配置日志记录
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

request = Request(**REQUEST_KWARGS)
bot = Bot(TOKEN, request=request)


def main() -> None:
    # 创建Updater并传入你的机器人的token
    updater = Updater(bot=bot, use_context=True)

    # 获取dispatcher来注册处理器
    dispatcher = updater.dispatcher

    # 注册不同的处理器
    dispatcher.add_handler(CommandHandler("start", hd.start))
    dispatcher.add_handler(CommandHandler("clear", hd.clear))
    dispatcher.add_handler(MessageHandler(Filters.voice & ~Filters.command, hd.handle_voice))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), hd.handle_text))

    # 开始接收信息并且不会停止
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
