from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton, ReplyKeyboardRemove
import logging, random, datetime


<<<<<<< HEAD
# Получение токена и текста со случайными ответами
TELEGRAM_TOKEN = open('res/token.txt').read()
with open('res/response.txt', 'r', encoding='utf-8') as f:
    neutral_response  = f.read().split('\n')
=======
#Получение токена и текста со случайными ответами
TELEGRAM_TOKEN = open("res/token.txt").read().strip()
with open('res/response.txt', 'r', encoding="utf-8") as f:
    insult_response  = (f.read()).split("\n")
>>>>>>> 0efabe0 (Add strip to token read)

with open('res/disprove.txt', 'r', encoding='utf-8') as f:
    disprove_response  = f.read().split('\n')

with open('res/kind.txt', 'r', encoding='utf-8') as f:
    kind_response  = f.read().split('\n')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)


def get_mode_keyboard():
    keyboard = [
        [
            InlineKeyboardButton('Добрый', callback_data='kind'),
            InlineKeyboardButton('Злой', callback_data='insult'),
            InlineKeyboardButton('Рандом', callback_data='random'),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def start(update, context):
    context.chat_data['mode'] = 'insult'
    context.chat_data['probability'] = 0.1
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text='Привет, меня зовут Кукко. Я — многофункциональный бот. Буду рад помочь')


def response(update, context):
    msg = update.message.text

    if random.random() < 0.1:
        if len(msg.split()) == 1 and context.chat_data['mode'] != 'kind':
            update.message.reply_text(f'{update.message.text} {random.choice(direct_response)}')
        else:
            if context.chat_data['mode'] == 'kind':
                kind(update)
            elif context.chat_data['mode'] == 'insult':
                insult(update)
            elif context.chat_data['mode'] == 'random' and random.random() < 0.5:
                kind(update)
            else:
                insult(update)



def keyboard_callback_handler(update, context):
    # Обработчик клавиатур

    query = update.callback_query
    data = query.data
    now = datetime.datetime.now()
    chat_id = update.effective_chat.id

    context.chat_data['mode'] = data
    query.message.edit_text(text=F'Режим сообщений был изменен на '{data}'')


def mode(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Выберите режим бота', reply_markup=get_mode_keyboard())


def insult(update):
    update.message.reply_text(random.choice(insult_response))


def kind(update):
    update.message.reply_text(random.choice(kind_response))


def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='В обычном режиме я иногда отвечаю на ваши сообщения')


def karelia(update, context):
    update.message.reply_text('Вы нашли пасхалку. Хайль Карелия! Voiten Kunnia! Слава Победе!')


def sticker(update, context):
    if random.random() < 0.15:
        update.message.reply_text('Крутой стикер, но у меня есть получше: https://t.me/addstickers/kukko_karelia')


def about(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Если есть какие-то вопросы, пишите в личку: @karelo_finnish_ssr')


def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('karelia', karelia))
    dp.add_handler(CommandHandler('mode', mode))
    dp.add_handler(CommandHandler('about', about))
    dp.add_handler(CallbackQueryHandler(callback=keyboard_callback_handler))
    dp.add_handler(MessageHandler(Filters.text, response))
    dp.add_handler(MessageHandler(Filters.photo, response))
    dp.add_handler(MessageHandler(Filters.sticker, sticker))

    updater.start_polling()
    logger.info('Kukko is running')
    updater.idle()


if __name__ == '__main__':
    main()
