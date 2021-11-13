from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
from pprint import pprint

from basic_search.Request import Request


def get_excel_data(path_to_excel_file: str):
    """
    Чтение excel файла и конвертация в лист. Самый простой вариант для работы с Excel
    :param path_to_excel_file: Путь до файла
    :return: Excel конвертированный в List
    """
    dataframe = pd.read_excel(path_to_excel_file)
    return dataframe.values.tolist()


def get_address(input_address: list):
    """
    конструктор адреса
    :param input_address: лист со строковыми, числовыми и значениями даты из ячеек Excel
    :return: строка с адресом для ввода в поле обычного поиска на сайте
    """
    a = ['' if i != i else i for i in input_address]

    if a[2] != 'Санкт-Петербург г' and a[2] != 'Москва г':
        # НЕстолица
        # Последнее слово всегда территориальная единица: край, область...
        region = a[2].replace(a[2].split(' ')[-1], '') + ', '
        city = str(a[3]) + '. ' + str(a[4])
    else:
        # CПБ и МСК
        region = ''
        city = a[2].replace(' г', '')
    street = str(a[5]) + '. ' + str(a[6])
    # Если в поле корпуса оказалась буква, то относим ее к номеру дома, а не создаем запись с "к. "
    if type(a[8]) is float or type(a[8]) is int:
        corpus = ', к. ' + str(int(a[8]))
    else:
        corpus = ''
    house = 'д. ' + str(a[7]) if a[8] is '' else 'д. ' + str(a[7]) + corpus
    return region + city + ', ' + street + ', ' + house


def find_house_by_address(req: Request, address: str):
    """
    Поиск дома по его адресу. Ввод адреса, нажатие на кнопку поиск и выбор первой строки таблицы на новой странице.
    :param req:
    :param address: сконструированный адрес
    :return: Если есть такой дом, то -> url, иначе -> ничего не возвращает
    """
    req.driver.get("https://www.reformagkh.ru/search")
    # Нажать на "Понятно" для cookie pop-up'a
    try:
        req.driver.find_element(By.CSS_SELECTOR, ".btn-cookie-submit").click()
    except NoSuchElementException:
        # print('cookie button not found')
        pass
    req.driver.find_element(By.NAME, "query").click()
    req.driver.find_element(By.NAME, "query").send_keys(address)
    req.driver.find_element(By.CSS_SELECTOR, ".f-16:nth-child(1)").click()
    # Поиск. Если ничего нет, то таблица на странице будет пустой
    try:
        req.driver.find_element(By.XPATH, "//td/a").click()
        req.driver.find_element(By.CSS_SELECTOR, ".tab-title:nth-child(1) > span").click()
        return req.driver.current_url
    except NoSuchElementException:
        print('=== === === === === UNABLE TO FIND HOUSE WITH ADDRESS', address)  # todo logic about house not found
        return None


def get_general_information(req: Request, result: dict, url: str):
    """
    Получение информации из раздела / Мой дом / Паспорт / Общие сведения
    :param req:
    :param result: шаблон ответа. Добавляем данные сюда
    :param url: где ищем
    :return:
    """
    req.driver.get(url)
    req.driver.find_element(By.ID, "common-tab").click()
    table = req.driver.find_element(By.XPATH, '/html/body/section[5]/div[2]/div/div[2]')
    raw_information = table.text
    splitted_info = raw_information.split('\n')
    for ix, s in enumerate(splitted_info):
        if 'эксплуатац' in s: result['Год ввода в эксплуатацию'] = splitted_info[ix + 1]
        if 'этаж' in s: result['Количество этажей'] = splitted_info[ix + 1]
        if 'тип постройки' in s: result['Серия, тип постройки здания'] = splitted_info[ix + 1]
        if 'Тип дома' in s: result['Тип дома'] = splitted_info[ix + 1]
        if 'кадастровый номер' in s:
            result['Кадастровый номер'] = splitted_info[ix + 1] if s != 'отсутствует' else None
        if 'аварий' in s:
            if splitted_info[ix + 1] == 'Да': result[
                'Дом признан аварийным'] = True
        if 'информация последний раз актуализировалась' in s:
            result['Последнее изменение анкеты'] = s.split(': ')[1]
    # Если статус дома не аварийный, то дать ему значение False
    if result['Дом признан аварийным'] != True: result['Дом признан аварийным'] = False
    return result


def get_construction_information(req: Request, result: dict, url: str):
    """
    Получение информации из Из раздела / Мой дом / Паспорт / Конструктивные элементы дома
    :param req:
    :param result: шаблон ответа. Добавляем данные сюда
    :param url: где ищем
    :return:
    """
    req.driver.get(url)
    req.driver.find_element(By.ID, "constructive-tab").click()
    table = req.driver.find_element(By.XPATH, '/html/body/section[5]/div[2]/div/div[2]')
    raw_information = table.text
    splitted_info = raw_information.split('\n')
    for ix, s in enumerate(splitted_info):
        if 'перекрытий' in s: result['Тип перекрытий'] = splitted_info[ix + 1]
        if 'несущих стен' in s: result['Материал несущих стен'] = splitted_info[ix + 1]
    return result


def get_information(path_to_excel: str):
    """
    Создние адреса для ввода в поисковое поле, затем проверка, есть ли такой дом через налилче возвращаемого url адреса
    :param path_to_excel: путь до excel файла
    :return: result - список домов с найденной информацией
    """
    address_data = get_excel_data(path_to_excel_file=path_to_excel)
    req = Request()
    req.setup_method()
    template = dict.fromkeys(
        ['Адрес',
         'Статус',
         'Год ввода в эксплуатацию',
         'Количество этажей',
         'Последнее изменение анкеты',
         'Серия, тип постройки здания',
         'Тип дома',
         'Дом признан аварийным',
         'Кадастровый номер',
         'Тип перекрытий',
         'Материал несущих стен'])
    result = []
    for a in address_data:
        address = get_address(a)
        url = find_house_by_address(req, address)
        data = template
        data['Адрес'] = address
        if url is not None:
            data['Статус'] = True
            data = get_general_information(req, data, url)
            data = get_construction_information(req, data, url)
            # print(address)
            # pprint(data)
            # print()
        else:
            data['Статус'] = False

        data_copy = data.copy()
        print(result)
        result.append(data_copy)
        print(result)
        print()

    req.teardown_method()
    return result


def print_information(path_to_excel: str):
    """
    Демонстрация работы функции выше
    :param path_to_excel:
    :return:
    """
    res = get_information(path_to_excel)
    # print('Удалось найти информацию о ', len(res), ' домах')
    pprint(res)
