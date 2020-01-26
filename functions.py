import requests
from bs4 import BeautifulSoup
import json
import pprint
import os
from telebot import types


def get_program_settings():
    """
    Получаем настройки программы
    :return: Возвращаем словарь с настройками
    """
    program_settings = {'path_to_token': os.path.join(os.getcwd(), 'Telegram_Token')}
    return program_settings


def load_token(path):
    '''
    Загружаем токен GitHub
    :param path: - путь до файла
    :return: - токен
    '''
    if os.path.exists(path):
        try:
            with open(path, 'r') as f:
                result = f.readline()
                return result
        except Exception as e:
            print(e)
            print('Файл с токеном Telegram не обнаружен!')


def read_json():
    with open('economic_result.json', 'r', encoding='utf-8') as f:
        result = json.load(f)
        pprint.pprint(result)


def write_json(result):
    with open('economic_result.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False)


def get_inner_url(domain, url):
    inner_response = requests.get(url)
    inner_soup = BeautifulSoup(inner_response.text, 'html.parser')

    # Получаем ссылку на картинку
    img = inner_soup.find('img', class_='topImg2')
    img_src = img['src']
    img_ref = f'{domain}{img_src}'

    result = []
    tbl = inner_soup.find('table')
    if tbl:
        i = 0
        for table_record in tbl.children:
            if i == 0:  # Первую итерацию с шапкой таблицы пропускаем
                i = + 1
                continue
            res_record = []
            data_records = table_record.find_all('td')
            # print(data_records)
            j = 0
            for data_record in data_records:
                if j == 2:
                    break
                res_record.append(data_record.text)
                j = + 1

            result.append(res_record)
            i = + 1

    return img_ref, result


def get_data_from_site(domain, user_choice):

    url = f'{domain}/stat.php?razdel=monthly&count={user_choice["country_code"]}'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    result = {}
    macro_indicators = {}
    result['title'] = f'Страна - {user_choice["country"]}. Период - {user_choice["period"]}'
    references = soup.find_all('a')
    for reference in references:
        img = reference.find('img')
        if img:
            inner_url = reference['href']
            macro_indicator = img['alt']

            inner_url = f'{domain}/{inner_url}&time={user_choice["period_code"]}'
            img_ref, inner_data = get_inner_url(domain, inner_url)
            macro_indicators[macro_indicator] = {'img': img_ref,
                                                 'indicator_data' : inner_data}

    result['macro_indicators'] = macro_indicators
    return result
    # В файл больше не записываем, результат возвращаем боту
    # Зписываем результат в JSON
    #write_json(result)
    # Считываем результат из JSON
    #read_json()


def get_text_for_reply(result_dict):
    list_text_for_reply = []

    #print(result_dict['macro_indicators'])
    macro_indicators = result_dict['macro_indicators']
    for indicator in macro_indicators:
        text_for_reply = f'*{result_dict["title"]}*\n\n'
        text_for_reply = f'{text_for_reply}*{indicator}*\n'
        values = macro_indicators[indicator]['indicator_data']
        for value in values:
            # TODO найти как вывести красивую таблицу.
            text_for_reply = f'{text_for_reply}{value}\n'
        list_text_for_reply.append([text_for_reply, macro_indicators[indicator]['img']])

    return list_text_for_reply


# Bot
def get_list_of_countries():
    return {'Россия': 'ru',
            'Германия': 'ge',
            'Япония': 'jp',
            'США': 'us',
            'Еврозона': 'ez',
            'Великобритания': 'uk'}


def get_period():
    return {'1 год': '0',
            '3 года': '1',
            '5 лет': '2',
            'Выбрать страну': 'back_to_country'}


def create_keyboard(type):
    if type == 'countries':
        buttons = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        buttons.add(*(get_list_of_countries().keys()))
    elif type == 'period':
        buttons = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        buttons.add(*(get_period().keys()))

    return buttons