from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from config import TOKEN, REQUEST_KWARGS
from telegram.utils.request import Request
import bot.handlers.handler as hd

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
