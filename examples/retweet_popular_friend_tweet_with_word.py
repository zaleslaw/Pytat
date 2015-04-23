# -*- coding: utf-8 -*-

__author__ = 'zaleslaw'

import tweepy


# Put here your Twitter's application keys
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''

# Put here word which is part of retweeted tweet
SEARCH_WORD = ''
# Define minimal number of favorites and retweets of searched tweet
FAVORITE_AMOUNT = 1
RETWEET_AMOUNT = 1
# Define number of explored last tweets in home_timeline
LAST_TWEETS_AMOUNT = 100

def is_popular(tweet):
    if tweet.favorite_count >= FAVORITE_AMOUNT and tweet.retweet_count >= RETWEET_AMOUNT:
        return True
    return False

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

api = tweepy.API(auth)
my_user_id = api.me().id

for status in tweepy.Cursor(api.home_timeline).items(LAST_TWEETS_AMOUNT):
    if status.user.id != my_user_id and SEARCH_WORD in status.text and is_popular(status):
        try:
            api.retweet(id=status.id)
            print(status.text)
        except tweepy.error.TweepError as e:
            print ("Error({0})".format(e.message))






