#!/usr/bin/python3

from urllib.request import urlopen
from urllib.error import HTTPError
from json import loads
from contextlib import closing
from time import sleep

def clean_words():
    with open("/usr/share/dict/words") as f:
        words = f.read().splitlines()
    words = filter(lambda x: x.isalpha(), words)
    words = filter(lambda x: x == x.lower(), words)
    return words

def is_cryptogram_of(*args):
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
    matches = []
    for w in clean_words():
        if is_cryptogram_of(w, target):
            matches.append(w)
    return matches

def check_twitter(handle):
    url = "https://twitter.com/users/username_available?username={0}"
    with urlopen(url.format(handle)) as f:
        response = loads(f.read().decode())
    return response["valid"]

if __name__ == "__main__":
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
