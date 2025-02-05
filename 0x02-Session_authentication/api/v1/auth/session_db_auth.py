#!/usr/bin/env python3
"""Module that defines the SessionDBAuth class
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
import os
from datetime import datetime, timedelta
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth class
    """

    def create_session(self, user_id: str = None) -> str:
        """Creates a session
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        user_session = UserSession(session_id=session_id, user_id=user_id)
        user_session.save()

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Gets user id by session id
        """
        status = super().user_id_for_session_id(session_id)

        if not status:
            return None

        user_sessions = UserSession.search({'session_id': session_id})
        if len(user_sessions) < 1:
            return None
        user_session = user_sessions[0]

        return user_session.user_id

    def destroy_session(self, request=None) -> bool:
        """Destroyes the session
        """
        status = super().destroy_session(request)
        if not status:
            return False

        session_id = self.session_cookie(request)
        user_sessions = UserSession.search({'session_id': session_id})
        if len(user_sessions) < 1:
            return False

        user_session = user_sessions[0]
        user_session.remove()
        return True
