#!/usr/bin/env python3
"""Module that obfuscates data
"""
import re
from typing import List
import logging
import mysql.connector
from os import environ

PII_FIELDS = ("name", "email", "password", "ssn", "phone")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """obfuscates data
    """
    message_chunks = re.split(separator, message)[:-1]
    chunks_count = len(message_chunks)
    new_message = ''
    for i in range(chunks_count):
        chunk = message_chunks[i]
        for field in fields:
            if (re.search('^{}=.*'.format(field), chunk)):
                chunk = re.sub('=.*', '={}'.format(redaction), chunk)
        new_message += '{};'.format(chunk)
    return new_message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Formats the log message"""
        return filter_datum(self.fields, self.REDACTION,
                            super(RedactingFormatter, self).format(record),
                            self.SEPARATOR
                            )


def get_logger() -> logging.Logger:
    """gets a new logger"""
    handler = logging.StreamHandler()
    logger = logging.getLogger('user_data')
    formatter = RedactingFormatter()
    handler.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Connects to mysql database"""
    username = environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
    pwd = environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    host = environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    name = environ.get('PERSONAL_DATA_DB_NAME')
    cnx = mysql.connector.connect(
        host=host,
        user=username,
        password=pwd,
        database=name)

    return cnx


def main():
    """Entry point"""

    cnx = get_db()
    cur = cnx.cursor()
    logger = get_logger()

    cur.execute('SELECT * from users')
    rows = cur.fecthall()
    for row in rows:
        msg = f"name={row[0]};email={row[1]};phone={row[2]};\
                ssn={row[3]};password={row[4];ip={row[5]};\
                last_login={row[6]};user_agent={row[7]};"
        logger.info(msg)

    cur.close()
    cnx.close()


if __name__ == '__main__':
    main()
