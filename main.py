from telegram.ext import Updater
from telegram.ext import CommandHandler
import logging

TELEGRAM_TOKEN = "1598899966:AAF-bvFOdrDX6yxwJQ4G-uBxBHikuV3_XQI"

#use_context - useful arg, =True needs for legacy code and old versions of the lib
updater = Updater(token=TELEGRAM_TOKEN, use_context=False)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет, меня зовут Кукко. Я - многофункциональный бот. Буду рад помочь")


def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()
    print("Kukko is running")
    updater.idle()


if __name__ == '__main__':
    main()
