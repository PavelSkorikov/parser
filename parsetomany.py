import requests
from bs4 import BeautifulSoup
import csv
from multiprocessing import Pool


def get_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
    r = requests.get(url, headers=headers)
    return r.text  # возвращает HTML код страницы

def get_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('div', class_='pagination-pages').find_all('a', class_='pagination-page')[-1].get('href')
    num_pages = pages.split('=')[1].split('&')[0]
    return int(num_pages)

def write_csv(data):
    with open('avito.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow((data['title'], data['price'], data['town'], data['url']))


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('div', class_='catalog-list').find_all('div', class_='item_table')
    for ad in ads:
        name = ad.find('div', class_='item_table-header').find('h3').text.strip().lower()
        if ('macbook' or 'макбук') in name:
            try:
                title = ad.find('div', class_='item_table-header').find('h3').text.strip()
            except:
                title = ''
            try:
                url = ad.find('div', class_='item_table-header').find('a').get('href')
            except:
                url = ''
            try:
                price = ad.find('div', class_='about').text.strip()
            except:
                price = ''
            try:
                town = ad.find('div', class_='data').find_all('p')[-1].text.strip()
            except:
                town = ''

            data = {'title': title,
                    'price': price,
                    'town': town,
                    'url': url}
            write_csv(data)
        else:
            continue


def main():
    url = 'https://www.avito.ru/rostovskaya_oblast/noutbuki?q=macbook'
    base_url = 'https://www.avito.ru/rostovskaya_oblast/noutbuki?'
    page_part = 'p='
    ask_part = '&q=macbook'

    total_pages = get_pages(get_html(url))

    for i in range(1, total_pages+1):
        url_gen = base_url + page_part + str(i) + ask_part
        html = get_html(url_gen)
        get_page_data(html)


if __name__ == '__main__':
    main()