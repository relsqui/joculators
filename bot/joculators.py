#!/usr/bin/python3

import tweepy

from secrets import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twitter = tweepy.API(auth)

twitter.update_status("Hello, Twitter.")
