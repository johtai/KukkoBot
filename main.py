from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton, ReplyKeyboardRemove
import logging, random, datetime, json, requests
from bs4 import BeautifulSoup
from telegram import ParseMode


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

# Получение токена
with open("secrets.json", "r") as read_file:
    TELEGRAM_TOKEN = json.load(read_file)["token"]

# Получения пароля
with open("secrets.json", "r") as read_file:
    superpassword = json.load(read_file)["superpassword"]

# Чтение файлов с ответами
with open('data/insult.txt', 'r', encoding='utf-8') as f:
    insult_response = f.read().strip().split('\n')

with open('data/disprove.txt', 'r', encoding='utf-8') as f:
    disprove_response = f.read().strip().split('\n')

with open('data/kind.txt', 'r', encoding='utf-8') as f:
    kind_response = f.read().strip().split('\n')

with open('data/photo.txt', 'r', encoding='utf-8') as f:
    photo_response = f.read().strip().split('\n')


def get_mode_keyboard():
    # Клавиатура с выбором режима
    keyboard = [
        [
            InlineKeyboardButton('Добрый', callback_data='kind'),
            InlineKeyboardButton('Злой', callback_data='insult'),
            InlineKeyboardButton('Рандом', callback_data='random'),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def start(update, context):
    context.chat_data['mode'] = 'random'
    context.chat_data['input'] = ''
    context.chat_data['admins'] = []
    context.chat_data['probability'] = 0.1
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text='Привет, меня зовут Кукко. Я — многофункциональный бот. Буду рад помочь')


def response(update, context):
    
    if not context.chat_data:
        start(update, context)

    msg = update.message.text

    if context.chat_data['input'] == 'admin':
        if msg == superpassword:
            context.chat_data['input'] = ''
            context.chat_data['admins'].append(update.message.from_user.id)
            context.bot.send_message(chat_id=update.effective_chat.id, text='Теперь вы админ')
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f'{msg}? Ты так сказал? Ха-ха, ну ты даешь)')

    elif random.random() < context.chat_data['probability']:
        if len(msg.split()) == 1 and context.chat_data['mode'] != 'kind':
            update.message.reply_text(f'{update.message.text} {random.choice(disprove_response)}')
        else:
            if context.chat_data['mode'] == 'kind':
                kind(update)
            elif context.chat_data['mode'] == 'insult':
                insult(update)
            elif context.chat_data['mode'] == 'random':
                choice = random.random()
                if choice < 0.5:
                    kind(update)
                else:
                    insult(update)



def photo(update, context):
    # if random.random() < context.chat_data['probability']:
    update.message.reply_text(random.choice(photo_response))


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


def photo(update, context):
    if random.random() < context.chat_data['probability']:
        update.message.reply_text(random.choice(photo_response))


def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='В обычном режиме я иногда отвечаю на ваши сообщения.')


def karelia(update, context):
    update.message.reply_text('Вы нашли пасхалку. Хайль Карелия! Voiten Kunnia! Слава Победе!')


def admin(update, context):
    if update.message.chat.type == 'private':
        context.chat_data['input'] = 'admin'
        context.bot.send_message(chat_id=update.effective_chat.id, text='Введите пароль админа')
        

def send(update, context):
    if update.message.chat.type == 'private' and update.message.from_user.id in context.chat_data["admins"]:
        context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text[5:])
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Кого ты пытаешься наебать?')


def info(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.to_json())


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
    context.bot.send_message(chat_id=update.effective_chat.id, text='Если есть какие-то вопросы, пишите в issues: https://github.com/johtai/KukkoBot')


def today(update, context):
    update.message.reply_text("\n".join(get_holiday()))


def isf(update, context):
    answer = random.choice(['Да', 'Нет', 'Да', 'Нет', 'Да', 'Нет', 'Да', 'Нет', 'Да', 'Нет', 'Да', 'Не знаю'])
    update.message.reply_text(answer)


def when(update, context):
    day = str(random.randint(1, 31))
    mon = str(random.randint(1, 12))
    year = random.randint(2022, 2050)

    if len(mon) == 1:
        mon = '0' + mon
    if len(day) == 1:
        day = '0' + day

    date = f'{day}.{mon}.{year}'
    answer = random.choice([date, date, date, date, date, date, date, 'Не знаю', 'Завтра', 'Послезавтра', 'Никогда', 'Скоро', 'Не'])

    update.message.reply_text(answer)

'''
def whois(update, context):
    msg = ' '.join(update.message.text.split()[1:])
    user = random.choice(USERS)

    text = get_whois(msg, user)

    update.message.reply_text(text)
'''

def get_whois(msg, user):
    delim = ' — '
    if len(msg.split()) > 1:
        delim = ' '
    return f'Я думаю, что {user}{delim}{msg}'


def get_holiday():
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    months = ["января", "февраля",  "марта",  "апреля",  "мая",  "июня",  "июля",  "августа",  "сентября",  "октяюря",  "ноября",  "декабря"]
    URL = f'https://ru.wikipedia.org/wiki/Категория:Праздники_{day}_{months[month - 1]}'
    html = requests.get(URL).text
    soup = BeautifulSoup(html, "html.parser")
    total = ["Праздники сегодня: \n"]

    holidays = soup.find_all("li")

    for tag in holidays:
        if "Праздники " in tag.text:
            break
        total.append("— " + tag.text)

    if len(total) > 10:
        return ["Сегодня праздников нет :/"]

    return total


def callback_day(context):
    context.bot.send_message(chat_id=-1001472999369, text="\n".join(get_holiday()))


def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    # dp.add_handler(CommandHandler('whois', whois))
    dp.add_handler(CommandHandler('is', isf))
    dp.add_handler(CommandHandler('when', when))
    dp.add_handler(CommandHandler('karelia', karelia))
    dp.add_handler(CommandHandler('mode', mode))
    dp.add_handler(CommandHandler('about', about))
    dp.add_handler(CommandHandler('admin', admin))
    dp.add_handler(CommandHandler('send', send))
    dp.add_handler(CommandHandler('info', info))
    dp.add_handler(CommandHandler('today', today))
    dp.add_handler(CommandHandler('probability', set_probability, pass_args=True))
    dp.add_handler(CallbackQueryHandler(callback=keyboard_callback_handler))
    dp.add_handler(MessageHandler(Filters.text, response))
    dp.add_handler(MessageHandler(Filters.photo, photo))
    # dp.add_handler(MessageHandler(Filters.sticker, sticker))

    timer = updater.job_queue
    timer.run_repeating(callback_day, interval=60*60*10, first=60)

    updater.start_polling()
    logger.info('Kukko is running')
    updater.idle()


if __name__ == '__main__':
    main()
