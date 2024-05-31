#!/usr/bin/python3
"""Defines the DBStorage class."""

from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """Interacts with the MySQL database."""

    __engine = None
    __session = None

    def __init__(self):
        """Creates the engine connection."""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:3306/{}'
                                      .format(getenv('HBNB_MYSQL_USER'),
                                              getenv('HBNB_MYSQL_PWD'),
                                              getenv('HBNB_MYSQL_HOST'),
                                              getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)

    def all(self, cls=None):
        """Returns a dictionary of all objects of a given class."""
        if cls:
            objs = self.__session.query(cls).all()
        else:
            classes = [BaseModel, User, State, City, Amenity, Place, Review]
            objs = []
            for c in classes:
                objs += self.__session.query(c).all()
        return {"{}.{}".format(type(obj).__name__, obj.id): obj for obj in objs}

    def new(self, obj):
        """Adds an object to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commits all changes to the current database session."""
        self.__session.commit()

    def reload(self):
        """Creates all tables in the database."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Calls remove() method on the private session attribute."""
        self.__session.remove()

