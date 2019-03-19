#!/usr/bin/env python3

from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
Base = declarative_base()


class Restaurant(Base):
    __tablename__ = 'restaurant'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False, primary_key=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }


class MenuItem(Base):
    __tablename__ = 'menu_item'
    name = Column(String)
    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restaurant = relationship(Restaurant)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'course': self.course
        }

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)


def db_setup():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    session.commit()
    result = session.query(MenuItem).all()
    return result
