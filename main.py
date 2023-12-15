from selenium import webdriver
from bs4 import BeautifulSoup

'''
# создание файла со ссылками на карточки
href_list = open("href_list.txt", 'w')
href_list.close()
'''

# создание файла для записи инфы о товарах
art_info_list = open("art_info_list.txt", 'w')
art_info_list.close()

'''
# получение страницы со ссылками на все карточки
for i in range(1, 15):

    url = 'https://www.stolplit.ru/supplier/E1-138/?PAGEN_1=' + str(i)
    # настройка веб драйвера селениум
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run Chrome in headless mode
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
        href_list.close()
'''

# открытие для чтения файла со ссылками
href_list = open("href_list.txt", 'r')

# получение инфы о товарах
for line in href_list:
    # Open the file containing the href links
    with open('href_list.txt', 'r') as file:
        href_list = file.readlines()

    # Инициализация веб-драйвера Chrome
    art_driver = webdriver.Chrome()

    # Открытие выходного файла, чтобы записать извлеченную информацию.
    output_file = open('art_info_list.txt', 'a')

    # Переброр всех ссылок href
    for href in href_list:
        # Перейти на страницу
        art_driver.get(href)
        art_page_source = art_driver.page_source

        # Close the webdriver
        # art_driver.quit()

        # Разберите исходный код страницы с помощью BeautifulSoup
        art_soup = BeautifulSoup(art_page_source, 'html.parser')

        # Извлеките элементы, используя заданные селекторы
        element1 = art_soup.find('div', {'class': 'table--td js-product-article'}).get_text(strip=True)

        # сделать трай кэтч блок
        size_element = art_soup.select_one('body > div.site-wrapper > div.site-content > div > div.page--product-detail > div.grid.grid--product > div.grid--product__info > div > div.tab__wrapper > div.tab__content.tab__content--active > div > div.characteristics__left > div.table.table-params > div:nth-child(2) > div > div:nth-child(2) > div').text.strip()
        # size_element = art_soup.select_one('body > div.site-wrapper > div.site-content > div > div.page--product-detail > div.grid.grid--product > div.grid--product__info > div > div.tab__wrapper > div > div > div > b > b > b > div > div:nth-child(2) > div > div:nth-child(2) > div').text.strip()

        # Запишите ссылку и извлеченные элементы в выходной файл
        with open('art_info_list.txt', 'a') as file:
            #file.write(f'{href.strip()} {size_element}\n')
            file.write(f'{href.strip()} {element1} {size_element}\n')

    # Закройте выходной файл и веб-драйвер
    output_file.close()
    art_driver.quit()
