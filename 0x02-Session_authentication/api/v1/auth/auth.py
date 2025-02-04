#!/usr/bin/env python3
"""Authentication
"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """request authentication for specfic paths
        """
        status = True
        if not path:
            return status
        elif path[-1] != '/':
            path += '/'
        if excluded_paths:
            for excluded_path in excluded_paths:

                if path == excluded_path:
                    status = False
                    break

                if excluded_path[-1] == '*':
                    path_part = excluded_path[:-1]
                    if path_part in path:
                        status = False
                        break

        return status

    def authorization_header(self, request=None) -> str:
        """Adds the autorization header to the request
        """
        if request and 'Authorization' in request.headers:
            return request.headers['Authorization']
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Gets the current user
        """
        return None

    def session_cookie(self, request=None) -> str:
        """Gets the coockie from the session
        """
        if request is None:
            return None

        cookie_name = os.environ.get('SESSION_NAME', '_my_session_id')
        session_id = request.cookies.get(cookie_name)

        return session_id
