from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, MessageHandler
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup
import logging, random


TELEGRAM_TOKEN = open("res/token.txt").read()
"logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)"


with open("res/response.txt") as r:
    random_text = r.read()


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
    if update.message["chat"]["type"] != "private":
        if random.randint(1, 100) > 10:
            update.message.reply(random.choice(random_text))


def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="safemode is running")


if __name__ == '__main__':
    main()
