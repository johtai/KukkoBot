from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, MessageHandler
from telegram import ReplyKeyboardMarkup
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
        reply_markup=ReplyKeyboardMarkup([["/help"], ["/insult"], ["/wholesome"]], resize_keyboard=True))
    context.chat_data["mode"] = "normal"


def insult_f(update, context):
    if context.chat_data["mode"] == "insult":
        update.message.reply_text("Режим агрессивного общения уже установлен")
    else:
        update.message.reply_text("Осторожно. Это режим оскорблений и ненависти. Вам может быть неприятно")
        context.chat_data["mode"] = "insult" 
    

def wholesome(update, context):
    if context.chat_data["mode"] == "wholesome":
        update.message.reply_text("Режим вежливого общения уже установлен")
    else:
        update.message.reply_text("Теперь я общаюсь вежливо")
        context.chat_data["mode"] = "wholesome" 
    

def response(update, context):
    if random.randint(1, 100) > 80:
        if context.chat_data["mode"] == "normal":
            update.message.reply_text("Скучно тут у вас")
        if context.chat_data["mode"] == "insult":
            update.message.reply_text(random.choice(insult))
        elif context.chat_data["mode"] == "wholesome":
            update.message.reply_text(random.choice(kind))
    print(context.chat_data)


def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="У меня есть несколкьо режимов общения:")


if __name__ == '__main__':
    main()
