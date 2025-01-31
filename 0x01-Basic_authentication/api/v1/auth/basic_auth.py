#!/usr/bin/env python3
"""Module that defines the BasicAuth class
"""
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """BasicAuth class
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Extracts the authorization header value"""
        auth = authorization_header
        if auth or isinstance(auth, str) or auth[:6] == 'Basic ':
            return auth[6:]
        return None

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Decodes base64 authorization header value"""
        value = base64_authorization_header
        if not value or not isinstance(value, str):
            return None

        value_bytes = value.encode('ascii')
        try:
            str_bytes = base64.b64decode(value_bytes)
            return str_bytes.decode('ascii')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """Extracts the user credentials"""
        value = decoded_base64_authorization_header
        if not value or not isinstance(value, str) or ':' not in value:
            return None, None

        credentials = value.split(':')
        return tuple(credentials)
