import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Boolean, Integer, String, Column, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship, sessionmaker, Session
from sqlalchemy import select, func, Integer, Table, Column, MetaData
from database.orm_objects import HouseInfo, Base
from basic_search.Request import Request
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
    req = Request()
    req.setup_method()

    addresses = pd.read_excel(path_to_excel_file).values.tolist()
    for a in addresses:
        r = get_information(req, a)
        house_information_object = HouseInfo(
            # kind_premises=a[0],
            # adress_postcode=a[1],
            # adress_region=a[2],
            # adress_type_city=a[3],
            # adress_city=a[4],
            # adress_type_street=a[5],
            # adress_street=a[6],
            # adress_house=a[7],
            # adress_block=a[8],
            # adress_flat=a[9],
            # adress=a[10],  # old address from Excel Table
            address=r['Адрес'],  # new address constructed by my script
            region=r['Регион'],
            city=r['Город'],
            street=r['Улица'],
            status=r['Статус'],
            year_of_occupancy=r['Год ввода в эксплуатацию'],
            number_of_floors=r['Количество этажей'],
            last_update=r['Последнее изменение анкеты'],
            type_of_construction=r['Серия, тип постройки здания'],
            house_type=r['Тип дома'],
            wreck_status=r['Дом признан аварийным'],
            cadastral_number=r['Кадастровый номер'],
            type_of_cellings=r['Тип перекрытий'],
            walls_material=r['Материал несущих стен']
        )
        db_session.add(house_information_object)
        db_session.commit()
        # house_information_list.append(house_information_object)
    # db_session.add_all(house_information_list)
    # db_session.commit()
    req.teardown_method()


def main():
    # Оставил исключительно для тестов
    engine = create_engine("postgresql+psycopg2://aydar:1234@localhost:5432/aydar")
    Base.metadata.create_all(engine)
    db_session = Session(engine)
    conn = engine.connect()

    path_to_excel_file = '../res/test.xlsx'

    load_data_to_db(path_to_excel_file, engine)


if __name__ == '__main__':
    main()
