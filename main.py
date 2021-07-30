from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, MessageHandler
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup
import logging, random


TELEGRAM_TOKEN = open("res/token.txt").read()
"logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)"


def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, response))

    updater.start_polling()
    print("Kukko is running")
    updater.idle()


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет, меня зовут Кукко. Я - многофункциональный бот. Буду рад помочь.")


def response(update, context):
    print(update.message)
    print("123")
    print(update.message["chat"]["type"])


def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="safemode is running")


if __name__ == '__main__':
    main()
