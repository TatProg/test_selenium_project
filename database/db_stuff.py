import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Boolean, Integer, String, Column, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship, sessionmaker, Session
from sqlalchemy.sql import select
from database.orm_objects import Addresses, HouseInfo, Base
from pprint import pprint

from basic_search.data_grabber import get_information


def load_data_to_db(path_to_excel_file: str, engine):
    """
    Чтение данных из Excel, поиск по reforma_zkh, обработка и внесение в PostgreSQL
    :param path_to_excel_file:
    :param engine:
    :return:
    """
    db_session = Session(engine)
    addresses = pd.read_excel(path_to_excel_file).values.tolist()
    res = get_information(path_to_excel_file)
    addresses_list, house_information_list = [], []

    for args in addresses:
        a = ['' if i != i else i for i in args]
        address = Addresses(
            KindPremises=a[0],
            Adress_PostCode=a[1],
            Adress_Region=a[2],
            Adress_TypeCity=a[3],
            Adress_City=a[4],
            Adress_TypeStreet=a[5],
            Adress_Street=a[6],
            Adress_House=a[7],
            Adress_Block=a[8],
            Adress_Flat=a[9],
            Adress=a[10])
        addresses_list.append(address)

    for a, r in zip(addresses_list, res):
        house_information_object = HouseInfo(
            address_id=a.id,
            status=r['Статус'],
            year_of_occupancy=r['Год ввода в эксплуатацию'],
            number_of_floors=r['Количество этажей'],
            last_update=r['Последнее изменение анкеты'],
            type_of_construction=r['Серия, тип постройки здания'],
            house_type=r['Тип дома'],
            wreck_status=r['Дом признан аварийным'],
            cadastral_number=r['Кадастровый номер'],
            type_of_ceilings=r['Материал несущих стен'],
            walls_material=r['Тип перекрытий']
        )
        house_information_list.append(house_information_object)
    pprint(house_information_list)
    db_session.add_all(addresses_list)
    db_session.add_all(house_information_list)
    db_session.commit()


def main():
    engine = create_engine("postgresql+psycopg2://aydar:1234@localhost:5432/aydar")
    Base.metadata.create_all(engine)

    path_to_excel_file = '/Users/aydar/Documents/PyCharmProjects/test_selenium_project/res/test_copy.xlsx'
    # addresses = pd.read_excel(path_to_excel_file).values.tolist()

    load_data_to_db(path_to_excel_file, engine)

    db_session = Session(engine)
    conn = engine.connect()


if __name__ == '__main__':
    main()
