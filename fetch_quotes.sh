#!/bin/bash

curl -s "https://en.wikiquote.org/wiki/$1" | ./extract_tweetables.py > "quotes/$1"
if [[ "$(stat --printf='%s' quotes/$1)" -eq 1 ]]; then
    rm "quotes/$1"
    echo "No suitable quotes."
else
    wc -l "quotes/$1" | cut -f 1 -d " " | tr -d "\n"
    echo " quotes fetched."
fi
