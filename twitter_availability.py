#!/usr/bin/python3

"""
Twitter handle availability checker.
(c) 2017 Finn Ellis.
"""

import logging

from urllib.request import urlopen
from urllib.error import HTTPError
from json import loads
from time import sleep

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

def check_twitter(handle, i=None, total=None):
    """
    Check whether a handle is available on Twitter. This does NOT do its own rate
    limiting; don't call it more than once per second.

    Args:
        The handle to check (a string).

    Returns:
        True if the handle is available on Twitter, False otherwise.
    """
    url = "https://twitter.com/users/username_available?username={0}"
    with urlopen(url.format(handle)) as f:
        response = loads(f.read().decode())
    prefix = "({i}/{total}) ".format(i=i, total=total) if i and total else ""
    status = "available!" if response["valid"] else "taken."
    logger.debug("%sChecking %s on Twitter ... %s", prefix, handle, status)
    return response["valid"]

if __name__ == "__main__":
    """
    Read words from stdin, check if they're available as Twitter handles, and
    return them preceded by either Y (if so) or N (if not).
    """
    import sys

    handles = sys.stdin.read().splitlines()
    i = 1
    total = len(handles)
    first = True
    for handle in handles:
        first = False if first else sleep(60)
        try:
            print("Y" if check_twitter(handle, i, total) else "N", handle)
            i = i + 1
        except HTTPError as e:
            print(e)
            break
