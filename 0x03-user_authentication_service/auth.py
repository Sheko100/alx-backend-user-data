#!/usr/bin/env python3
"""Module that handles the authentication
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hashes a password
    """
    if not password or not isinstance(password, str):
        return None

    hash_pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    return hash_pwd
