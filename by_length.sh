#!/bin/bash

# Adapted from http://stackoverflow.com/a/5917762/252125

cat quotes/* | awk '{ print length, $0 }' | sort -nr -s | cut -d" " -f2-
