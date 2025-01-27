#!/usr/bin/env python3
"""Module that encrypts
"""
import bcrypt


def hash_password(pwd: str) -> bytes:
    """encryptes password
    """
    hashed = bcrypt.hashpw(pwd.encode("utf-8"), bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validates the password hash
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
