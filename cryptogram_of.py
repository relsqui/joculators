#!/usr/bin/python3

"""
Cryptogram finder. (c) 2017 Finn Ellis.
"""

import logging

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

if __name__ == "__main__":
    """
    Take a word on the command line and return cryptograms preceded by Y or N,
    indicating whether they're available as Twitter handles.
    """
    import sys
    print("\n".join(find_cryptograms(sys.argv[1])))
