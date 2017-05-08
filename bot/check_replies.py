#!/usr/bin/python3

import tweepy
import random
import cryptograms

from secrets import *

twitter = None
past_tweets = None
affirmatives = ["Nice.", "Good job!", "That's correct.", "Yep!", "You got it."]

def init_api():
    """
    Initializes the twitter global with an authenticated API object.
    """
    global twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    twitter = tweepy.API(auth)

def init_history():
    """
    Initilizes the dictionary of tweet history.
    """
    global past_tweets
    past_tweets = {}
    with open("tweet_history") as f:
        history = f.read().splitlines()
    for tweet in history:
        tid, text = tweet.split("\t")
        past_tweets[tid] = text

def send_reply(tweet, message):
    """
    Sends a reply to the given tweet. The author's username is automatically
    prepended.

    Args:
        tweet - A tweet object.
        message - A string to send.

    Returns:
        The tweet that was sent.
    """
    text = "@{0} {1}".format(tweet.author.screen_name, message)
    return twitter.update_status(text, in_reply_to_status_id=tweet.id)

def check_accuracy(tweet):
    target_id = tweet.in_reply_to_status_id_str
    if not target_id or target_id not in past_tweets.keys():
        return False
    tweet_text = tweet.text.split("@joculators", 1)[1].strip().upper()
    normal_target = cryptograms.normalize(past_tweets[target_id])
    normal_reply = cryptograms.normalize(tweet_text)
    return normal_target == normal_reply

def confirm_replies():
    with open("last_reply_id") as f:
        last_seen = int(f.read().strip())
    tweets = twitter.search("to:joculators", since_id=last_seen)
    to_verify = []
    last_id = 0
    for tweet in tweets:
        if check_accuracy(tweet):
            try:
                send_reply(tweet, random.choice(affirmatives))
                print("confirmed tweet", tweet.id, "from ", tweet.author.screen_name)
            except tweepy.Error.TweepError as e:
                if e.message[0]["code"] == 187:
                    print("skipped sending duplicate reply to tweet", tweet.id, "from ", tweet.author.screen_name)
                else:
                    print(e)
        if tweet.id > last_id:
            last_id = tweet.id
    if last_id:
        with open("last_reply_id", "w") as f:
            f.write(str(last_id))

def main():
    init_api()
    init_history()
    confirm_replies()

if __name__ == "__main__":
    main()
