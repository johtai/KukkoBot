from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, MessageHandler
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup
import logging, random


TELEGRAM_TOKEN = open("res/token.txt").read()
"logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)"


with open('res/insults.txt', 'r', encoding="utf-8") as f:
    insult = (f.read()).split("\n")


with open('res/kind.txt', 'r', encoding="utf-8") as f:
    kind = (f.read()).split("\n")


def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("insult", insult_f))
    dp.add_handler(CommandHandler("wholesome", wholesome))
    dp.add_handler(MessageHandler(Filters.text, response))

    updater.start_polling()
    print("Kukko is running")
    updater.idle()


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет, меня зовут Кукко. Я - многофункциональный бот. Буду рад помочь.", \
        reply_markup=InlineKeyboardMarkup([["/help"]], resize_keyboard=True))


def response(update, context):
    print(context.chat_data)


def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="safemode")


if __name__ == '__main__':
    main()
