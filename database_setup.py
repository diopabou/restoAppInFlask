import sys
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Restaurant(Base):
    __tablename__ = 'restaurant'
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)

class MenuItem(Base):
    __tablename__ = 'menu_item'
    id = Column(Integer, primary_key= True)
    name = Column(String(80), nullable = False)
    description = Column(String(200))
    price = Column(String(8))
    course = Column(String(200))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

engine = create_engine('sqlite:///restomenu.db')
Base.metadata.create_all(engine)
