#!/usr/bin/python3

"""
Cryptogram finder and Twitter handle checker. Because I needed both at once.
(c) 2017 Finn Ellis.
"""

import logging

from urllib.request import urlopen
from urllib.error import HTTPError
from json import loads
from contextlib import closing
from time import sleep

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

def clean_words():
    """
    Filter /usr/share/dict words for lines which only contain ASCII letters.

    Returns:
        A list of such strings.
    """
    logger.info("Getting word list and filtering ...")
    words = []
    with open("/usr/share/dict/words") as f:
        for word in f:
            word = word[:-1]
            if word.isalpha() and word == word.lower() and all(ord(c) < 128 for c in word):
                words.append(word)
    logger.info("Loaded %s words.", len(words))
    return words

def is_cryptogram_of(*args):
    """
    Verify whether a set of strings are cryptograms of each other.

    Args:
        Any number of strings.

    Returns:
        True if all strings are cryptograms of each other, False otherwise.
    """
    for a in args:
        if len(a) != len(args[0]):
            return False
    ords = list(map(lambda x: list(map(ord, x)), args))
    maps = [{} for a in args]
    for i in range(len(args[0])):
        for j in range(len(args)):
            if ords[j][i] not in maps[j].keys():
                maps[j][ords[j][i]] = i
            ords[j][i] = maps[j][ords[j][i]]
    for o in ords:
        if o != ords[0]:
            return False
    return True

def find_cryptograms(target):
    """
    Find cryptograms of a target string. Uses the sanitized wordlist provided
    by clean_words (lowercase ASCII only from /usr/share/dict/words).

    Args:
        One target word.

    Returns:
        A list of cryptograms of that word.
    """
    matches = []
    logger.info("Looking for cryptograms of %s.", target)
    for w in clean_words():
        if is_cryptogram_of(w, target):
            matches.append(w)
    logger.info("Found %s cryptograms.", len(matches))
    return matches

def check_twitter(handle):
    """
    Check whether a handle is available on Twitter. This does NOT do its own rate
    limiting; don't call it more than once per second.

    Args:
        The handle to check (a string).

    Returns:
        True if the handle is available on Twitter, False otherwise.
    """
    url = "https://twitter.com/users/username_available?username={0}"
    logger.debug("Checking %s on Twitter ...", handle)
    with urlopen(url.format(handle)) as f:
        response = loads(f.read().decode())
    return response["valid"]

if __name__ == "__main__":
    """
    Take a word on the command line and return cryptograms preceded by Y or N,
    indicating whether they're available as Twitter handles.
    """
    import sys
    target = sys.argv[1]
    matches = find_cryptograms(target)
    try:
        for m in matches:
            print("Y" if check_twitter(m) else "N", m)
            sleep(1)
    except HTTPError as e:
        print(e)
        print(e.headers)
