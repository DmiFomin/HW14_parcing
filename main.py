import requests
from bs4 import BeautifulSoup
import pprint
import functions as fn

DOMAIN = 'http://www.ereport.ru/'
url = f'{DOMAIN}stat.php?razdel=monthly&count=ru'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

result = {}
references = soup.find_all('a')
for reference in references:
    img = reference.find('img')
    if img:
        inner_url = reference['href']
        title = img['alt']

        inner_url = f'{DOMAIN}{inner_url}&time=2'  # Берем данные за пять лет
        inner_data = fn.get_inner_url(inner_url)
        result[title] = inner_data

# Зписываем результат в JSON
fn.write_json(result)
# Считываем результат из JSON
fn.read_json()

