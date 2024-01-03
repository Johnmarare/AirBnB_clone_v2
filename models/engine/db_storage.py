#!/usr/bin/python3
"""Defines the DBStorage engine."""
from os import getenv
from models.base_model import Base
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker


class DBStorage:
    """Represents a database storage engine

    Attributes:
        __engine: engine.
        __session: session.
    """

    __engine = None
    __session = None

    def __init__(self):
        """Initialize a DBStorage instance"""
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
                                      format(getenv("HBNB_MYSQL_USER"),
                                             getenv("HBNB_MYSQL_PWD"),
                                             getenv("HBNB_MYSQL_HOST"),
                                             getenv("HBNB_MYSQL_DB")),
                                      pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session(self.__session)
        all objects depending of the class name (argument cls)
        if not cls query all types of objects(User...)
        Return:
            Dict lasses in format <class name>.<obj id> = obj
        """
        objects = {}

        if cls:
            if type(cls) is str:
                cls = eval(cls)
            query = self.__session.query(cls)
            for elem in query:
                key = "{}.{}".format(type(elem).__name__, elem.id)
                objects[key] = elem
        else:
            lists = [State, City, User, Place, Review, Amenity]
            for obj in lists:
                query = self.__session.query(obj)
                for elem in query:
                    key = "{}.{}".format(type(elem).__name__, elem.id)
                    objects[key] = elem
        return (objects)

    def new(self, obj):
        """Add object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes to the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete object from the current database session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in db and init"""
        Base.metadata.create_all(self.__engine)
        session_f = sessionmaker(bind=self.__engine,
                                 expire_on_commit=False)
        Session = scoped_session(session_f)
        self.__session = Session()

    def close(self):
        """close session                                                                    """
        self.__session.close()
