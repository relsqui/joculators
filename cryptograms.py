#!/usr/bin/python3

"""
Cryptogram finder.
(c) 2017 Finn Ellis.

A "cryptogram" for the purpose of this module is a string which can be
transformed into a target string by consistently replacing each letter 1:1
with another letter (or with itself).
"""

import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


def clean_words():
    """
    Filter /usr/share/dict words for lines which only contain lowercase ASCII.

    Returns:
        A list of such strings.
    """
    logger.info("Getting word list and filtering ...")
    words = []
    with open("/usr/share/dict/words") as f:
        for word in f:
            word = word[:-1]
            if (word.isalpha() and word == word.lower() and
               all(ord(c) < 128 for c in word)):
                words.append(word)
    logger.info("Loaded %s words.", len(words))
    return words


def normalize(string):
    """
    Convert a string into a normalized cryptogram form, in which each letter is
    consistently replaced by the first position at which that letter appears in
    the string. That is, the first letter is replaced by 1, the second is
    replaced by 2 (unless it's the same as the first, in which case it's also
    1), the third is replaced by 3 (unless it's the same as a previous letter),
    and so on. The output of this process for two different strings is
    identical if and only if the strings are cryptograms of each other.

    Args:
        A string.

    Returns:
        A list of integers, the normal form of the string.
    """
    ords = list(map(ord, string))
    cipher = {}
    for i in range(len(string)):
        if ords[i] not in cipher:
            cipher[ords[i]] = i
        ords[i] = cipher[ords[i]]
    return ords


def find_cryptograms(target):
    """
    Find cryptograms of a target string in the sanitized wordlist provided
    by clean_words (lowercase ASCII only from /usr/share/dict/words).

    Args:
        One target word.

    Returns:
        A list of cryptograms of that word.
    """
    matches = []
    logger.info("Looking for cryptograms of %s.", target)
    normal_target = normalize(target)
    for w in clean_words():
        if normalize(w) == normal_target:
            matches.append(w)
    logger.info("Found %s cryptograms.", len(matches))
    return matches

if __name__ == "__main__":
    """
    Take a word on the command line and return any cryptograms of it which are
    in the cleaned-up version of /usr/share/dict/words.
    """
    import sys
    print("\n".join(find_cryptograms(sys.argv[1])))
