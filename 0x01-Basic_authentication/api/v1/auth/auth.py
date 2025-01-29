#!/usr/bin/env python3
"""Authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """request authentication for specfic paths
        """
        if not path:
            return True
        elif path[-1] != '/':
            path += '/'
        if excluded_paths and path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """Adds the autorization header to the request
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Gets the current user
        """
        return None
