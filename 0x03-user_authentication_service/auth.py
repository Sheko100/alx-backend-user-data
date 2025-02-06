#!/usr/bin/env python3
"""Module that handles the authentication
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _generate_uuid() -> str:
    """generates an id
    """
    return str(uuid.uuid4())


def _hash_password(password: str) -> bytes:
    """Hashes a password
    """
    if not password or not isinstance(password, str):
        return None

    hash_pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    return hash_pwd


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """registers the user
        """
        db = self._db
        try:
            user = db.find_user_by(email=email)
            raise ValueError('User {} already exists'.format(email))
        except NoResultFound:
            hash_pwd = _hash_password(password)
            user = db.add_user(email, hash_pwd)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Validates the login attempt
        """

        try:
            user = self._db.find_user_by(email=email)
            hashed = user.hashed_password
            if bcrypt.checkpw(password.encode('utf-8'), hashed):
                return True
        except Exception:
            pass

        return False

    def create_session(self, email: str) -> str:
        """Creates a session
        """

        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            user.session_id = session_id
            return session_id
        except Exception:
            pass
