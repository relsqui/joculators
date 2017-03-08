#!/bin/bash

curl -s "https://en.wikiquote.org/wiki/$1" | ./extract_tweetables.py > "quotes/$1"
wc -l "quotes/$1" | cut -f 1 -d " " | tr -d "\n"
echo " quotes fetched."
