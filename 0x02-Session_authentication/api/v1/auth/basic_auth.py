#!/usr/bin/env python3
"""Module that defines the BasicAuth class
"""
from api.v1.auth.auth import Auth
from models.user import User
import base64
from typing import TypeVar


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

        credentials = value.split(':', 1)
        return tuple(credentials)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Gets a user object based on credentials"""
        email_valid = user_email and isinstance(user_email, str)
        pwd_valid = user_pwd and isinstance(user_pwd, str)

        if not email_valid or not pwd_valid:
            return None

        users = User.search({'email': user_email})
        if len(users) < 1:
            return None

        user = users[0]

        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves a User instance"""
        header_value = self.authorization_header(request)
        if header_value:
            auth_value = self.extract_base64_authorization_header(header_value)
            auth_text = self.decode_base64_authorization_header(auth_value)
            user_credentials = self.extract_user_credentials(auth_text)
            user = self.user_object_from_credentials(
                    user_email=user_credentials[0],
                    user_pwd=user_credentials[1])
            return user
