from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton, ReplyKeyboardRemove
import logging, random, datetime


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

# Получение токена
TELEGRAM_TOKEN = open('token.txt').read().strip()

# Чтение файлов с ответами
with open('data/insult.txt', 'r', encoding='utf-8') as f:
    insult_response = f.read().strip().split('\n')

with open('data/disprove.txt', 'r', encoding='utf-8') as f:
    disprove_response = f.read().strip().split('\n')

with open('data/kind.txt', 'r', encoding='utf-8') as f:
    kind_response = f.read().strip().split('\n')

with open('data/trash.txt', 'r', encoding='utf-8') as f:
    trash_response = f.read().strip().split('\n')

with open('data/photo.txt', 'r', encoding='utf-8') as f:
    photo_response = f.read().strip().split('\n')


def get_mode_keyboard():
    # Клавиатура с выбором режима
    keyboard = [
        [
            InlineKeyboardButton('Добрый', callback_data='kind'),
            InlineKeyboardButton('Злой', callback_data='insult'),
            InlineKeyboardButton('Треш', callback_data='trash'),
            InlineKeyboardButton('Рандом', callback_data='random'),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def start(update, context):
    context.chat_data['mode'] = 'random'
    context.chat_data['probability'] = 0.1
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text='Привет, меня зовут Кукко. Я — многофункциональный бот. Буду рад помочь')


def response(update, context):
    if not context.chat_data:
        start(update, context)

    msg = update.message.text

    if random.random() < context.chat_data['probability']:
        if len(msg.split()) == 1 and context.chat_data['mode'] != 'kind':
            update.message.reply_text(f'{update.message.text} {random.choice(disprove_response)}')
        else:
            if context.chat_data['mode'] == 'kind':
                kind(update)
            elif context.chat_data['mode'] == 'insult':
                insult(update)
            elif context.chat_data['mode'] == 'trash':
                trash(update)
            elif context.chat_data['mode'] == 'random':
                choice = random.random()
                if choice < 0.33:
                    kind(update)
                elif choice < 0.66:
                    insult(update)
                else:
                    trash(update)


def photo_response(update, context):
    if random.random() < context.chat_data['probability']:
        photo(update)


def keyboard_callback_handler(update, context):
    # Обработчик клавиатур

    query = update.callback_query
    data = query.data

    context.chat_data['mode'] = data
    query.message.edit_text(text=f"Режим сообщений был изменен на '{data}'")


def mode(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Выберите режим бота', reply_markup=get_mode_keyboard())


def insult(update):
    update.message.reply_text(random.choice(insult_response))


def kind(update):
    update.message.reply_text(random.choice(kind_response))


def trash(update):
    update.message.reply_text(random.choice(trash_response))


def photo(update):
    update.message.reply_text(random.choice(photo_response))


def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='В обычном режиме я иногда отвечаю на ваши сообщения.')


def karelia(update, context):
    update.message.reply_text('Вы нашли пасхалку. Хайль Карелия! Voiten Kunnia! Слава Победе!')


def sticker(update, context):
    if random.random() < 0.1:
        update.message.reply_text('Крутой стикер, но у меня есть получше: https://t.me/addstickers/kukko_karelia')


def set_probability(update, context):
    if not context.args:
        update.message.reply_text(f'Текущая вероятность: {str(int(context.chat_data["probability"] * 100)) + "%" if "probability" in context.chat_data else "не установлена"}.')
    else:
        try:
            probability = float(context.args[0])
            context.chat_data['probability'] = probability
            update.message.reply_text(f'Установил вероятность ответа {int(probability * 100)}%.')
        except:
            update.message.reply_text('Чё-то хуйня какая-то произошла.')


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
    dp.add_handler(CommandHandler('probability', set_probability, pass_args=True))
    dp.add_handler(CallbackQueryHandler(callback=keyboard_callback_handler))
    dp.add_handler(MessageHandler(Filters.text, response))
    dp.add_handler(MessageHandler(Filters.photo, photo_response))
    dp.add_handler(MessageHandler(Filters.sticker, sticker))

    updater.start_polling()
    logger.info('Kukko is running')
    updater.idle()


if __name__ == '__main__':
    main()
