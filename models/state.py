#!/usr/bin/python3
""" State Module for HBNB project """
from models.city import City
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.orm import relationship
from os import getenv
import models


class State(BaseModel, Base):
    """"Represents city
    Attributes:
        __tablename__: The name of table states
        name: name of state
        cities: cities
    """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship("City",  backref="state", cascade="delete")
    else:
        @property
        def cities(self):
            """
            Getter attribute that returns the list of City instances with stat
            _id equals
            to the current State.id for FileStorage.
            """
            from models import storage
            cList = []
            for city in list(storage.all("City").values()):
                if city.state.id == self.id:
                    cList.append(city)
            return cList
