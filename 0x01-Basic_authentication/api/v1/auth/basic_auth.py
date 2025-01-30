#!/usr/bin/env python3
"""Module that defines the BasicAuth class
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """BasicAuth class
    """
    pass

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Extracts the authorization header value"""
        auth = authorization_header
        if not auth or not isinstance(auth, str) or auth[:6] != 'Basic ':
            return None
        return auth[6:]
