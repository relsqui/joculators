#!/usr/bin/python3

import tweepy
import random

from secrets import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twitter = tweepy.API(auth)

with open("for_consuming") as f:
    grams = f.read().splitlines()

random.shuffle(grams)
to_tweet = grams.pop()

tweet = twitter.update_status(to_tweet)

with open("for_consuming", "w") as f:
    f.write("\n".join(grams))

with open("tweet_history", "a") as f:
    f.write("{0}\t{1}\n".format(tweet.id, to_tweet))
