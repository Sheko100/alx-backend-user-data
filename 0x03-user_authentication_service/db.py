#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email, hashed_password) -> User:
        """Adds a new user to the databse
        """
        session = self._session
        user = User(
                email=email,
                hashed_password=hashed_password,
                session_id=None,
                reset_token=None
                )
        session.add(user)

        session.commit()

        return user

    def find_user_by(self, **kwargs) -> User:
        """Gets a user
        """
        session = self._session
        attr_dict = {}
        col_names = User.__table__.columns

        if len(kwargs) < 1:
            return

        col_name = list(kwargs.keys())[0]
        if len(kwargs) > 1 or col_name not in col_names:
            raise InvalidRequestError

        attr_dict[col_name] = kwargs[col_name]

        user = session.query(User).filter_by(**attr_dict).first()

        if (user is None):
            raise NoResultFound

        return user

    def update_user(self, id, **kwargs) -> None:
        """Updates the user data
        """
        session = self._session
        col_names = User.__table__.columns

        for key in kwargs:
            if key == "id" or key not in col_names:
                raise ValueError

        user = self.find_user_by(id=id)

        for key in kwargs:
            setattr(user, key, kwargs[key])

        session.commit()
