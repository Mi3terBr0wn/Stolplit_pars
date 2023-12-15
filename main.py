import random
from selenium import webdriver
import requests
from bs4 import BeautifulSoup

# создание файла со ссылками на карточки
href_list = open("href_list.txt", 'w')
href_list.close()
# создание файла для записи инфы о товарах
art_info_list = open("art_info_list.txt", 'w')
art_info_list.close()
'''
# создание файла со страницей
main_file = open("main_file.txt", 'w')
main_file.close()


user_agent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
    ]
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

    '''
    # запись в файл всего html кода страницы
    main_file = 'main_file_' + str(i) + '.txt'
    with open(main_file, 'w') as file:
        file.write(str(soup))
    '''

    # нахождение ссылок изапись их в файл
    link_list = soup.find_all('a',
                              class_='btn btn-secondary--outline btn-md js-product-link')

    with open('href_list.txt', 'a') as file:
        for link in link_list:
            file.write('https://www.stolplit.ru/' + link['href'] + '\n')

    '''
    headers = {
        'User-Agent': random.choice(user_agent_list)
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    # htmlResponse = response.text
    # создание и открытие для записи файла для записи страницы со ссылками на все карточки
    # with open("main_file.txt", 'w') as main_file:
    #     main_file.write(htmlResponse)
    #     main_file.close()

    # Найти все ссылки с указанным классом и записать их в файл
    link_list = soup.find_all('a',
                              class_='btn btn-primary--outline btn-md--circle js-add-cart js-product-action-button')
    with open('href_list.txt', 'w') as file:
        for link in link_list:
            file.write(link['href'] + '\n')

    # Записать все HTML-содержимое страницы в файл.
    main_file = 'main_file_' + str(i) + '.txt'
    with open(main_file, 'w') as file:
        file.write(str(soup))

    with open("main_file.txt", 'r') as file:
    # чтение файла парсером
        soup = BeautifulSoup(main_file, 'html.parser')

        # открытие на запись файла со ссылками на карточки
        href_list = open("href_list.txt", 'a')

        # запись ссылок в файл
        href_tag = (soup.find(class_="product__buttons").
                    find(class_="btn btn-secondary--outline btn-md js-product-link"))
        for a in soup.find_all(href_tag):
            href_list.write(a.get('href') + '\n')
        
    '''
    # закрытие записи в файл
    href_list.close()

    # открытие для чтения файла со ссылками
    href_list = open("href_list.txt", 'r')

    # получение инфы о товарах
    for line in href_list:
        # запись ссылки в файл с инфой о товарах
        art_info_list = open("art_info_list.txt", 'a')
        art_info_list.write(str(line) + ' ')

        # настройка веб драйвера селениум
        art_options = webdriver.ChromeOptions()
        art_options.add_argument("--headless")  # Run Chrome in headless mode
        art_driver = webdriver.Chrome(options=options)

        # получение содержимого страницы
        art_driver.get(str(line))
        art_page_source = driver.page_source

        # закрытие веб драйвера
        art_driver.quit()
        # разбитие html cтраницы с помощью bs4
        art_soup = BeautifulSoup(page_source, 'html.parser')

        # получение тега элемента, содержащего артикул, и запись артикула в файл
        art_tag = art_soup.select_one('body > div.site-wrapper > div.site-content > div > div.page--product-detail > '
                                      'div.grid.grid--product > div.grid--product__info > div > div.tab__wrapper > '
                                      'div.tab__content.tab__content--active > div > div.characteristics__left > '
                                      'div.table.table-params > div:nth-child(1) > div:nth-child(2) >'
                                      'div.table--td.js-product-article > div')
        text = art_tag.get_text()
        with open('art_info_list.txt', 'a') as file:
            file.write(text + ' ')
        file.close()

        # ширина
        width_tag = art_soup.select_one('body > div.site-wrapper > div.site-content > div > div.page--product-detail > '
                                        'div.grid.grid--product > div.grid--product__info > div > div.tab__wrapper > '
                                        'div.tab__content.tab__content--active > div > div.characteristics__left > '
                                        'div.table.table-params > div:nth-child(2) > div > div:nth-child(2) > div >'
                                        'text(1)')
        text = width_tag.get_text()
        with open('art_info_list.txt', 'a') as file:
            file.write(text + ' ')
        file.close()

        # высота
        height_tag = art_soup.select('body > div.site-wrapper > div.site-content > div > div.page--product-detail > '
                                     'div.grid.grid--product > div.grid--product__info > div > div.tab__wrapper > '
                                     'div.tab__content.tab__content--active > div > div.characteristics__left > '
                                     'div.table.table-params > div:nth-child(2) > div > div:nth-child(2) > div > '
                                     'text(2)')
        text = height_tag.get_text()
        with open("art_info_list.txt", "a") as file:
            file.write(text + ' ')
        file.close()

        # глубина
        depth_tag = art_soup.select('body > div.site-wrapper > div.site-content > div > div.page--product-detail > '
                                    'div.grid.grid--product > div.grid--product__info > div > div.tab__wrapper > '
                                    'div.tab__content.tab__content--active > div > div.characteristics__left > '
                                    'div.table.table-params > div:nth-child(2) > div > div:nth-child(2) > div > '
                                    'text(3)')

        text = depth_tag.get_text()
        with open("art_info_list.txt", "a") as file:
            file.write(text + '\n')
        file.close()

        '''
        with open("art_info_file.txt", 'r') as art_info_file:
            # чтение файла с карточкой парсером
            soup = BeautifulSoup(art_info_file, 'html.parser')

            # получение тега элемента, содержащего артикул, и запись артикула в файл
            art_tag = soup.select_one('body > div.site-wrapper > div.site-content > div > div.page--product-detail > '
                                      'div.grid.grid--product > div.grid--product__info > div > div.tab__wrapper > '
                                      'div.tab__content.tab__content--active > div > div.characteristics__left > '                                          'div.table.table-params > div:nth-child(1) > div:nth-child(2) > '
                                      'div.table--td.js-product-article > div')
            with open("art_info_list.txt", "a") as art_info_list:
                art_info_list.write(art_tag.text + ' ')
            art_info_list.close()

            # ширина
            width_tag = soup.select_one('body > div.site-wrapper > div.site-content > div > div.page--product-detail > '
                                        'div.grid.grid--product > div.grid--product__info > div > div.tab__wrapper > '
                                        'div.tab__content.tab__content--active > div > div.characteristics__left > '                                            'div.table.table-params > div:nth-child(2) > div > div:nth-child(2) > div > '
                                        'text(1)')

            text = width_tag.get_text()
            with open("art_info_list.txt", "a") as art_info_list:
                art_info_list.write(text + ' ')
            art_info_list.close()

            # высота
            height_tag = soup.select('body > div.site-wrapper > div.site-content > div > div.page--product-detail > '
                                     'div.grid.grid--product > div.grid--product__info > div > div.tab__wrapper > '
                                     'div.tab__content.tab__content--active > div > div.characteristics__left > '
                                     'div.table.table-params > div:nth-child(2) > div > div:nth-child(2) > div > '
                                     'text(2)')
            text = width_tag.get_text()
            with open("art_info_list.txt", "a") as art_info_list:
                art_info_list.write(text + ' ')
            art_info_list.close()
            # глубина
            depth_tag = soup.select('body > div.site-wrapper > div.site-content > div > div.page--product-detail > '
                                    'div.grid.grid--product > div.grid--product__info > div > div.tab__wrapper > '
                                    'div.tab__content.tab__content--active > div > div.characteristics__left > '
                                    'div.table.table-params > div:nth-child(2) > div > div:nth-child(2) > div > '
                                    'text(3)')

            text = width_tag.get_text()
            with open("art_info_list.txt", "a") as art_info_list:
                art_info_list.write(text + '\n')
            art_info_list.close()
            '''
