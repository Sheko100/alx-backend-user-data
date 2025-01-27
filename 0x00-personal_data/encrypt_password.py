#!/usr/bin/env python3
"""Module that encrypts
"""
import bcrypt


def hash_password(pwd: str) -> bcrypt.hashpw:
    """encryptes password
    """
    hashed = bcrypt.hashpw(pwd.encode("utf-8"), bcrypt.gensalt())
    return hashed
