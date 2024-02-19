from selenium import webdriver
from bs4 import BeautifulSoup

# создание файла со ссылками на карточки
href_list = open("href_list.txt", 'w')
href_list.close()

# создание файла для записи ссылок на все цвета
all_href_list = open("all_href_list.txt", 'w')
all_href_list.close()


# создание файла для записи инфы о товарах
art_info_list = open("art_info_list.txt", 'w')
art_info_list.close()

# получение страницы со ссылками на все карточки
for i in range(14, 15):

    url = 'https://www.stolplit.ru/supplier/E1-138/?code=E1-138&PAGEN_1=' + str(i)
    # настройка веб драйвера селениум
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    # Run Chrome in headless mode
    driver = webdriver.Chrome(options=options)

    # получение содержимого страницы
    driver.get(url)
    page_source = driver.page_source

    # закрытие веб драйвера
    driver.quit()
    # разбитие html cтраницы с помощью bs4
    soup = BeautifulSoup(page_source, 'html.parser')

    # нахождение ссылок изапись их в файл
    link_list = soup.find_all('a',
                              class_='btn btn-secondary--outline btn-md js-product-link')

    with open('href_list.txt', 'a') as file:
        for link in link_list:
            file.write('https://www.stolplit.ru/' + link['href'] + '\n')
        # закрытие записи в файл
        file.close()

    with open('all_href_list.txt', 'a') as file:
        for link in link_list:
            file.write('https://www.stolplit.ru/' + link['href'] + '\n')
        # закрытие записи в файл
        file.close()

# открытие для чтения файла со ссылками
href_list = open("href_list.txt", 'r')

# получение инфы о товарах
for line in href_list:
    # Open the file containing the href links
    with open('href_list.txt', 'r') as file:
        href_list = file.readlines()

# Инициализация веб-драйвера Chrome
all_colors_driver = webdriver.Chrome()

# Открытие выходного файла, чтобы записать извлеченную информацию.
output_file = open('all_href_list.txt', 'a')

for href in href_list:

    # Open the file containing the href links
    with open('href_list.txt', 'r') as file:
        href_list = file.readlines()

    all_colors_driver.get(href)
    all_colors_page_source = all_colors_driver.page_source

    all_colors_page_soup = BeautifulSoup(all_colors_page_source, 'html.parser')

    # нахождение ссылок изапись их в файл
    all_link_list = all_colors_page_soup.find_all('a',
                                  class_='btn btn-color--xl js-color')

    with open('all_href_list.txt', 'a') as file:
        for link in all_link_list:
            file.write('https://www.stolplit.ru/' + link['href'] + '\n')
        # закрытие записи в файл
        file.close()

# закрытие веб драйвера
#all_colors_page_source.quit()

# открытие для чтения файла со ссылками
all_href_list = open("all_href_list.txt", 'r')
# Инициализация веб-драйвера Chrome
art_driver = webdriver.Chrome()
# Открытие выходного файла, чтобы записать извлеченную информацию.
output_file = open('art_info_list.txt', 'a')

# Переброр всех ссылок href
for href in all_href_list:
    # Переход на страницу
    art_driver.get(href)
    art_page_source = art_driver.page_source

    # закрытие веб драйвера
    # art_driver.quit()

    # Разбор исходного кода страницы с помощью BeautifulSoup
    art_soup = BeautifulSoup(art_page_source, 'html.parser')

    try:
        element1 = art_soup.find('div', {'class': 'table--td js-product-article'}).get_text(strip=True)
    except Exception:
        element1 = 'нет данных'

    try:
        size_element = art_soup.select_one(
            'body > div.site-wrapper > div.site-content > div > div.page--product-detail > div.grid.grid--product > div.grid--product__info > div > div.tab__wrapper > div.tab__content.tab__content--active > div > div.characteristics__left > div.table.table-params > div:nth-child(2) > div > div:nth-child(2) > div').text.strip()
    except Exception:
        size_element = 'нет данных'

    try:
        price_element = art_soup.select_one('#js-detail_product_price_wrapper > div')
    except Exception:
        price_element = 'нет данных'

    try:
        number_of_rating_element = art_soup.select_one(
            'body > div.site-wrapper > div.site-content > div > div.page--product-detail > div.grid.grid--product > div.grid--product__menu > div > div.product-menu__info.js-product-info > div.product-menu__meta.product-card-desktop > table > tbody > tr > td.rating-text > span.bx_stars_rating_votes').text.strip()
    except Exception:
        number_of_rating_element = 'нет данных'

    try:
        number_of_reviews_element = art_soup.select_one(
        'body > div.site-wrapper > div.site-content > div > div.page--product-detail > div.grid.grid--product > div.grid--product__menu > div > div.product-menu__info.js-product-info > div.product-menu__meta.product-card-desktop > table > tbody > tr > td.rating-text > span.link.js-rating').text.strip()
    except Exception:
        number_of_reviews_element = 'нет данных'

    # Запись ссылки и извлеченных элементов в выходной файл
    with open('art_info_list.txt', 'a') as file:
        #file.write(f'{href.strip()} {size_element}\n')
        #file.write(f'{href.strip()} {element1} {size_element} {price_element}\n')
        #file.write(f'{href.strip()} {element1} {size_element}\n')
        file.write(f'{href.strip()} {element1} {price_element} {size_element} {number_of_rating_element} {number_of_reviews_element}\n')
        #file.write(f'{href.strip()} {element1}\n')


# Закройте выходной файл и веб-драйвер
output_file.close()
art_driver.quit()
