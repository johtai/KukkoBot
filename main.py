from telegram.ext import Updater
from telegram.ext import CommandHandler
import logging


TELEGRAM_TOKEN = open("res/token.txt").read()
"logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)"


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет, меня зовут Кукко. Я - многофункциональный бот. Буду рад помочь", \
        reply_markup=["/commands", "/help"])


def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Бог в помощь")
    

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    updater.start_polling()
    print("Kukko is running")
    updater.idle()


if __name__ == '__main__':
    main()
