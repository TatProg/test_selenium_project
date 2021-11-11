from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd

from Request import Request


def get_excel_data(path_to_excel_file: str):
    """
    Чтение excel файла и конвертация в лист. Самый простой вариант для Excel -> Lists
    :param path_to_excel_file: Путь до файла
    :return: List
    """
    dataframe = pd.read_excel(path_to_excel_file)
    return dataframe.values.tolist()


def get_address(a: list):
    # Делаю лист со строками, иначе все переменные приводить к строкам
    # a = [str(i) for i in a]
    if a[2] != 'Санкт-Петербург г' and a[2] != 'Москва г':
        # НЕстолица
        # Последнее слово всегда территориальная единица: край, область...
        region = a[2].replace(a[2].split(' ')[-1], '')
        city = str(a[4])
        street = str(a[5]) + '. ' + str(a[6])
        house = 'д. ' + str(a[7])
        if a[8] == a[8]
            house += ', к.' + str(a[8])
        return region + ', ' + city + ', ' + street + ', ' + house
    else:
        # CПБ и МСК
        city = a[2].replace(' г', '')
        street = a[5] + '. ' + a[6]
        house = 'д. ' + a[7]
        if a[8] != 'nan':
            house += ', к.' + a[8]
        # город - тип адреса - улица - номер
        return city + ', ' + street + ', ' + house


def get_building_info(req: Request):
    building_information = []
    # 5 | click | xpath=//table[@id='searched-houses-advanced']/tbody/tr/td/a |
    # первая строка таблицы
    # /html/body/section[2]/div/table/tbody/tr/td[1]/a
    # req.driver.find_element(By.XPATH, "//*[@id=\'searched-houses-advanced\']/tbody/tr/td/a").click()
    # req.driver.find_element(By.CSS_SELECTOR, ".text-dark").click()
    req.driver.find_element(By.XPATH, "//td/a").click()
    # 6 | click | css=.tab-title:nth-child(1) > span |  |
    req.driver.find_element(By.CSS_SELECTOR, ".tab-title:nth-child(1) > span").click()

    # 14 | storeText | css=#list-common-passport > #profile-house-style .border-bottom-grey:nth-child(4) > td:nth-child(2) | !year
    # Год ввода дома в эксплуатацию
    building_information.append(req.driver.find_element(By.CSS_SELECTOR,
                                                        "#list-common-passport > #profile-house-style .border-bottom-grey:nth-child(4) > td:nth-child(2)").text)
    # 15 | storeText | css=#list-common-passport > #profile-house-style .font-weight-bold > td:nth-child(2) | !change
    # Последнее изменение анкеты
    building_information.append(req.driver.find_element(By.CSS_SELECTOR,
                                                        "#list-common-passport > #profile-house-style .font-weight-bold > td:nth-child(2)").text)
    # 16 | storeText | css=#list-common-passport > #profile-house-style .border-bottom-grey:nth-child(9) > td:nth-child(2) | !floors
    # количество этажей
    building_information.append(req.driver.find_element(By.CSS_SELECTOR,
                                                        "#list-common-passport > #profile-house-style .border-bottom-grey:nth-child(9) > td:nth-child(2)").text)
    # 17 | storeText | css=#list-common-passport > #profile-house-style .border-bottom-grey:nth-child(8) > td:nth-child(2) | !number
    # Серия
    building_information.append(req.driver.find_element(By.CSS_SELECTOR,
                                                        "#list-common-passport > #profile-house-style .border-bottom-grey:nth-child(8) > td:nth-child(2)").text)
    # 18 | storeText | css=#list-common-passport > #profile-house-style .border-bottom-grey:nth-child(5) > td:nth-child(2) | !type
    # Тип дома
    building_information.append(req.driver.find_element(By.CSS_SELECTOR,
                                                        "#list-common-passport > #profile-house-style .border-bottom-grey:nth-child(5) > td:nth-child(2)").text)

    # Todo Add "Дом признан аварийным" and "Кадастровый номер"

    # 19 | clickAt | id=constructive-tab |
    req.driver.find_element(By.ID, "constructive-tab").click()
    # 20 | storeText | css=#house-passport-constructive .sub-tr:nth-child(3) > td:nth-child(2) | !foundation
    # Тип фундамента
    building_information.append(req.driver.find_element(By.CSS_SELECTOR,
                                                        "#house-passport-constructive .sub-tr:nth-child(3) > td:nth-child(2)").text)
    # 21 | storeText | css=#house-passport-constructive .sub-tr:nth-child(5) > td:nth-child(2) | !walls
    # Тип перекрытий
    building_information.append(req.driver.find_element(By.CSS_SELECTOR,
                                                        "#house-passport-constructive .sub-tr:nth-child(5) > td:nth-child(2)").text)
    # 22 | storeText | css=.sub-tr:nth-child(6) > td:nth-child(2) | !wallz
    # Материал несущих стен
    building_information.append(req.driver.find_element(By.CSS_SELECTOR, ".sub-tr:nth-child(6) > td:nth-child(2)").text)

    return building_information
