import requests
from bs4 import BeautifulSoup
import json
import pprint


def read_json():
    with open('economic_result.json', 'r', encoding='utf-8') as f:
        result = json.load(f)
        pprint.pprint(result)


def write_json(result):
    with open('economic_result.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False)


def get_inner_url(url):
    inner_response = requests.get(url)
    inner_soup = BeautifulSoup(inner_response.text, 'html.parser')

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

    return result