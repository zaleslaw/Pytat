# -*- coding: utf-8 -*-

__author__ = 'zaleslaw'

import tweepy
from pymongo import MongoClient


# Put here your Twitter's application keys
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''

# Put here username of Twitter user whose tweets are interested for you
TWITTER_USER_NAME = ''

# Change host and port of your Mongo instance database if it is required
MONGO_PORT = 27017
MONGO_HOST = 'localhost'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

api = tweepy.API(auth)

user = api.get_user(TWITTER_USER_NAME)


print ("Username is " + str(user.screen_name))
print ("Number of followers is " + str(user.followers_count))
print ("Number of friends is " + str(user.friends_count))
print ("Number of tweets is " + str(user.statuses_count))

tweets = {}
for tweet in tweepy.Cursor(api.user_timeline, id=TWITTER_USER_NAME, wait_on_rate_limit=True).items():
    tweets[str(tweet.created_at)] = tweet.text

print("Number of dumped tweets is " + str(len(tweets)))

client = MongoClient(MONGO_HOST, MONGO_PORT)
db = client['tweets']
tweet_collection = db[TWITTER_USER_NAME]

for key, value in sorted(tweets.items()):
    tweet = {"created_at": key,
             "text": value,
    }
    tweet_collection.insert(tweet)







