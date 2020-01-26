import functions as fn
import telebot
from telebot import apihelper, types
import pprint


# Записываем настройки
PROGRAM_SETTINGS = fn.get_program_settings()
TOKEN = fn.load_token(PROGRAM_SETTINGS['path_to_token'])

DOMAIN = 'http://www.ereport.ru'

proxies = {
 'http': 'http://148.217.94.54:3128',
 'https': 'http://148.217.94.54:3128',
}

apihelper.proxy = proxies
bot = telebot.TeleBot(TOKEN)

# Заисываем в глобальную переменную
USER_CHOICE = {}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Создаем клавиатуру
    buttons = fn.create_keyboard('countries')
    bot.reply_to(message, f'Добро пожаловать, {str(message.from_user.first_name)}! Выберите страну:', reply_markup=buttons)


@bot.message_handler(commands=['info'])
def info(message):
    bot.reply_to(message, '*MacroEconomicsBot*\nБот выводит информацию по макроэкономическим показателям ведущих стран мира. Данные берутся с сайта http://www.ereport.ru', parse_mode="Markdown")


@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, '*Команды бота:*\n/start - начало работы с ботом\n/help - информация по командам\n/info - информацуия о боте', parse_mode="Markdown")


@bot.message_handler(content_types=['text'])
def reverse_text(message):

    if fn.get_period().get(message.text) == 'back_to_country':
        buttons = fn.create_keyboard('countries')
        bot.reply_to(message, 'Выберите страну:', reply_markup=buttons)
    elif fn.get_list_of_countries().get(message.text):
        # Получаем из словаря код страны
        USER_CHOICE['country'] = message.text
        USER_CHOICE['country_code'] = fn.get_list_of_countries().get(message.text)
        buttons = fn.create_keyboard('period')
        bot.reply_to(message, f'{message.text}. Выберите период:', reply_markup=buttons)
    elif fn.get_period().get(message.text):
        # Получаем период из словаря
        USER_CHOICE['period'] = message.text
        USER_CHOICE['period_code'] = fn.get_period().get(message.text)
        result_dict = fn.get_data_from_site(DOMAIN, USER_CHOICE)
        #pprint.pprint(result_dict)
        list_text_for_reply = fn.get_text_for_reply(result_dict)

        for text_for_reply in list_text_for_reply:
            #bot.reply_to(message, text_for_reply[0], parse_mode="Markdown")
            bot.send_photo(message.chat.id, text_for_reply[1], text_for_reply[0], parse_mode="Markdown")


bot.polling()



