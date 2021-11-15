from sqlalchemy import Table, Boolean, Integer, String, Column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class HouseInfo(Base):
    __tablename__ = 'house_information'
    address_id = Column(Integer, primary_key=True)
    # Old data from Excel
    # kind_premises = Column(String(256))
    # adress_postcode = Column(String(256))
    # adress_region = Column(String(256))
    # adress_type_city = Column(String(256))
    # adress_city = Column(String(256))
    # adress_type_street = Column(String(256))
    # adress_street = Column(String(256))
    # adress_house = Column(String(256))
    # adress_block = Column(String(256))
    # adress_flat = Column(String(256))
    # adress = Column(String(256))  # old address from Excel Table
    # New data starts here:
    address = Column(String(256))  # new address constructed by my script
    region = Column(String(256))
    city = Column(String(256))
    street = Column(String(256))
    status = Column(Boolean)
    year_of_occupancy = Column(Integer)
    number_of_floors = Column(Integer)
    last_update = Column(String(256))
    type_of_construction = Column(String(256))
    house_type = Column(String(256))
    wreck_status = Column(Boolean)
    cadastral_number = Column(String(256))
    type_of_cellings = Column(String(256))
    walls_material = Column(String(256))
