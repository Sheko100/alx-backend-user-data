#!/usr/bin/env python3
"""Defines User model
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declartive_base()


class User(base):
    """User Model"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=true)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    session_id = Column(String, nullable=True)
    reset_token = Column(String, nullable=True)
