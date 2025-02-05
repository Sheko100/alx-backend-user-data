#!/usr/bin/env python3
"""Module that defines the SessionExpAuth class
"""
from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta
from models.user import User


class SessionExpAuth(SessionAuth):
    """SessionExpAuth class
    """
    user_id_by_session_id = {}

    def __init__(self):
        """Initialization
        """
        try:
            session_duration = int(os.environ.get('SESSION_DURATION', 0))
        except ValueError:
            session_duration = 0

        self.session_duration = session_duration

    def create_session(self, user_id: str = None) -> str:
        """Creates a session
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        date = datetime.now()
        self.user_id_by_session_id[session_id] = {'user_id': user_id,
                                                  'created_at': date}

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Gets user id by session id
        """

        if not session_id or session_id not in self.user_id_by_session_id:
            return None

        session_dict = self.user_id_by_session_id[session_id]

        if self.session_duration <= 0:
            return session_dict['user_id']

        if 'created_at' not in session_dict:
            return None

        duration = timedelta(seconds=self.session_duration)
        expire_date = session_dict['created_at'] + duration

        if expire_date < datetime.now():
            return None

        return session_dict['user_id']
