#!/usr/bin/env python3
"""Module that obfuscates data
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: List[str], separator: str) -> str:
    """obfuscates data
    """
    message_chunks = re.split(separator, message)
    chunks_count = len(message_chunks)
    new_message = ''
    for i in range(chunks_count):
        chunk = message_chunks[i]
        for field in fields:
            if (re.search('^{}=.*'.format(field), chunk)):
                chunk = re.sub('=.*', '={}'.format(redaction), chunk)

        new_message += '{};'.format(chunk)

    return new_message
