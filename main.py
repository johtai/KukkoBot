from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton
import logging, random


#Получение токена и текста со случайными ответами
TELEGRAM_TOKEN = open("res/token.txt").read()
with open('res/response.txt', 'r', encoding="utf-8") as f:
    random_text  = (f.read()).split("\n")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет, меня зовут Кукко. Я — многофункциональный бот. Буду рад помочь")


def response(update, context):
    if update.message["chat"]["type"] != "private":
        if random.random() < 0.15:
            update.message.reply_text(random.choice(random_text))


def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="В обычном режиме я иногда отвечаю на ваши сообщения")


def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, response))

    updater.start_polling()
    print("Kukko is running")
    updater.idle()


if __name__ == '__main__':
    main()
