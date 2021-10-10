from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton
import logging, random


#Получение токена и текста со случайными ответами
TELEGRAM_TOKEN = open("res/token.txt").read()
with open('res/response.txt', 'r', encoding="utf-8") as f:
    random_text  = (f.read()).split("\n")

with open('res/direct_response.txt', 'r', encoding="utf-8") as f:
    direct_response  = (f.read()).split("\n")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет, меня зовут Кукко. Я — многофункциональный бот. Буду рад помочь")


def response(update, context):
    msg = update.message.text
    #print(msg)

    if random.random() < 0.1:
        if len(msg) == 1:
            update.message.reply_text(f'{update.message.text} {random.choice(direct_response)}')
        else:
            update.message.reply_text(random.choice(random_text))


def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="В обычном режиме я иногда отвечаю на ваши сообщения")


def karelia(update, context):
    update.message.reply_text("Вы нашли пасхалку. Хайль Карелия! Voiten Kunnia! Слава Победе!")


def sticker(update, context):
    if random.random() < 0.15:
        update.message.reply_text("Крутой стикер, но у меня есть получше: https://t.me/addstickers/kukko_karelia")


def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("karelia", karelia))
    dp.add_handler(MessageHandler(Filters.text, response))
    dp.add_handler(MessageHandler(Filters.photo, response))
    dp.add_handler(MessageHandler(Filters.sticker, sticker))

    updater.start_polling()
    print("Kukko is running")
    updater.idle()


if __name__ == '__main__':
    main()
