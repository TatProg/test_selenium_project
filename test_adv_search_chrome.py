# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
from pprint import pprint
import os
import chromedriver_binary


# openpyxl
# geckodriver bc of Mozilla
# pip install chromedriver-binary

class Request_Advanced_Search:
    def setup_method(self):
        path_to_gecko = '/usr/local/bin/geckodriver'
        # self.driver = webdriver.Firefox(executable_path=path_to_gecko)
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self):
        self.driver.quit()

    def test(self):
        pass


def get_excel_data(path_to_excel_file: str):
    """
    Чтение excel файла и конвертация в лист. Самый простой вариант для Excel -> Lists
    :param path_to_excel_file: Путь до файла
    :return: List
    """
    dataframe = pd.read_excel(path_to_excel_file)
    return dataframe.values.tolist()


def get_building_info(raq: Request_Advanced_Search):
    building_information = []
    # 12 | clickAt | xpath=//table[@id='searched-houses-advanced']/tbody/tr/td/a |
    # первая строка таблицы
    raq.driver.find_element(By.XPATH, "//table[@id=\'searched-houses-advanced\']/tbody/tr/td/a").click()
    # 13 | clickAt | css=.tab-title:nth-child(1) > span |
    # паспорт
    raq.driver.find_element(By.CSS_SELECTOR, ".tab-title:nth-child(1) > span").click()
    # 14 | storeText | css=#list-common-passport > #profile-house-style .border-bottom-grey:nth-child(4) > td:nth-child(2) | !year
    # Год ввода дома в эксплуатацию
    building_information.append(raq.driver.find_element(By.CSS_SELECTOR,
                                                        "#list-common-passport > #profile-house-style .border-bottom-grey:nth-child(4) > td:nth-child(2)").text)
    # 15 | storeText | css=#list-common-passport > #profile-house-style .font-weight-bold > td:nth-child(2) | !change
    # Последнее изменение анкеты
    building_information.append(raq.driver.find_element(By.CSS_SELECTOR,
                                                        "#list-common-passport > #profile-house-style .font-weight-bold > td:nth-child(2)").text)
    # 16 | storeText | css=#list-common-passport > #profile-house-style .border-bottom-grey:nth-child(9) > td:nth-child(2) | !floors
    # количество этажей
    building_information.append(raq.driver.find_element(By.CSS_SELECTOR,
                                                        "#list-common-passport > #profile-house-style .border-bottom-grey:nth-child(9) > td:nth-child(2)").text)
    # 17 | storeText | css=#list-common-passport > #profile-house-style .border-bottom-grey:nth-child(8) > td:nth-child(2) | !number
    # Серия
    building_information.append(raq.driver.find_element(By.CSS_SELECTOR,
                                                        "#list-common-passport > #profile-house-style .border-bottom-grey:nth-child(8) > td:nth-child(2)").text)
    # 18 | storeText | css=#list-common-passport > #profile-house-style .border-bottom-grey:nth-child(5) > td:nth-child(2) | !type
    # Тип дома
    building_information.append(raq.driver.find_element(By.CSS_SELECTOR,
                                                        "#list-common-passport > #profile-house-style .border-bottom-grey:nth-child(5) > td:nth-child(2)").text)

    # Todo Add "Дом признан аварийным" and "Кадастровый номер"

    # 19 | clickAt | id=constructive-tab |
    raq.driver.find_element(By.ID, "constructive-tab").click()
    # 20 | storeText | css=#house-passport-constructive .sub-tr:nth-child(3) > td:nth-child(2) | !foundation
    # Тип фундамента
    building_information.append(raq.driver.find_element(By.CSS_SELECTOR,
                                                        "#house-passport-constructive .sub-tr:nth-child(3) > td:nth-child(2)").text)
    # 21 | storeText | css=#house-passport-constructive .sub-tr:nth-child(5) > td:nth-child(2) | !walls
    # Тип перекрытий
    building_information.append(raq.driver.find_element(By.CSS_SELECTOR,
                                                        "#house-passport-constructive .sub-tr:nth-child(5) > td:nth-child(2)").text)
    # 22 | storeText | css=.sub-tr:nth-child(6) > td:nth-child(2) | !wallz
    # Материал несущих стен
    building_information.append(raq.driver.find_element(By.CSS_SELECTOR, ".sub-tr:nth-child(6) > td:nth-child(2)").text)

    return building_information


# def construct_request(df: pd.DataFrame):
def construct_request(addresses):
    for a in addresses:
        raq = Request_Advanced_Search()
        raq.setup_method()
        # 1 | open | https://www.reformagkh.ru/search/houses-advanced |
        raq.driver.get("https://www.reformagkh.ru/search/houses-advanced")

        # гипотеза: если город не фед значения, то надо больше данных вводить
        region, city = '', ''
        if a[2] != 'Санкт-Петербург г' and a[2] != 'Москва г':
            # Последнее слово всегда территориальная единица: край, область...
            region = a[2].replace(a[2].split(' ')[-1], '')
            city = a[4]
            print('shit shit shit shit shit shit shit shit')
        else:
            # cookie error
            wait = WebDriverWait(raq.driver, 100)
            element = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, ".btn-cookie-submit")))
            raq.driver.find_element(By.CSS_SELECTOR, ".btn-cookie-submit").click()
            # raq.driver.find_element(By.XPATH('/html/body/div[4]/div/div/div[2]/div/button')).click();

            # 2b | type | id=edit-region | Санкт-Петербург
            city = a[2].replace(' г', '')
            raq.driver.find_element(By.ID, "edit-region").click()
            raq.driver.find_element(By.ID, "edit-region").send_keys(city)
            # 3 | sendKeys | id=edit-region | ${KEY_DOWN}
            raq.driver.find_element(By.ID, "edit-region").send_keys(Keys.DOWN)
            # 4 | sendKeys | id=edit-region | ${KEY_TAB}
            raq.driver.find_element(By.ID, "edit-region").send_keys(Keys.TAB)
            # 5 | type | id=edit-street | Репищева (ул)
            street = str(a[6]) + ' (' + str(a[5]) + ')'
            raq.driver.find_element(By.ID, "edit-street").click()
            raq.driver.find_element(By.ID, "edit-street").send_keys(street)
            # 6 | sendKeys | id=edit-street | ${KEY_DOWN}
            raq.driver.find_element(By.ID, "edit-street").send_keys(Keys.DOWN)
            # 7 | sendKeys | id=edit-street | ${KEY_TAB}
            raq.driver.find_element(By.ID, "edit-street").send_keys(Keys.TAB)

        # 8 | type | id=edit-house | Дом 21 Корпус 1
        building = 'Дом ' + str(a[7])
        # Самая простая проверка на поле NaN - сравнить переменную саму с собой
        if a[8] == a[8]:
            building = 'Дом ' + str(a[7]) + ' Корпус ' + str(a[8])
        raq.driver.find_element(By.ID, "edit-house").send_keys(building)
        # 9 | sendKeys | id=edit-house | ${KEY_DOWN}
        raq.driver.find_element(By.ID, "edit-house").send_keys(Keys.DOWN)
        # 10 | sendKeys | id=edit-house | ${KEY_TAB}
        raq.driver.find_element(By.ID, "edit-house").send_keys(Keys.TAB)
        # 11 | click | css=.px-5:nth-child(6) |
        raq.driver.find_element(By.CSS_SELECTOR, ".px-5:nth-child(6)").click()

        info = get_building_info(raq)
        print(info)

        raq.teardown_method()
    pass


def test_selenium():
    t = Request_Advanced_Search()
    t.setup_method()
    t.teardown_method()


if __name__ == '__main__':
    foo = get_excel_data(path_to_excel_file='/Users/aydar/Desktop/поиск Работы/Тестовая выборка.xlsx')
    # test_selenium()
    construct_request(foo)