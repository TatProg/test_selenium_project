from sqlalchemy import create_engine, MetaData, Table, Boolean, Integer, String, Column, DateTime, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from sqlalchemy.orm import relationship

Base = declarative_base()


class Addresses(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    KindPremises = Column(String(64))
    Adress_PostCode = Column(String(64))
    Adress_Region = Column(String(64))
    Adress_TypeCity = Column(String(64))
    Adress_City = Column(String(64))
    Adress_TypeStreet = Column(String(64))
    Adress_Street = Column(String(64))
    Adress_House = Column(String(64))
    Adress_Block = Column(String(64))
    Adress_Flat = Column(String(64))
    Adress = Column(String(256))
    info = relationship('HouseInfo', uselist=False)
    # info = relationship('HouseInfo', backref='addresses', uselist=False)


class HouseInfo(Base):
    __tablename__ = 'house_info'
    id = Column(Integer, primary_key=True)  # todo проверить, нужно ли это поле
    address_id = Column(Integer(), ForeignKey('addresses.id'))
    status = Column(Boolean)
    year_of_occupancy = Column(Integer)
    number_of_floors = Column(Integer)
    last_update = Column(String(64))
    type_of_construction = Column(String(64))
    house_type = Column(String(64))
    wreck_status = Column(Boolean)
    cadastral_number = Column(String(64))
    type_of_ceilings = Column(String(64))
    walls_material = Column(String(64))
