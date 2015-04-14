# -*- coding: utf-8 -*-

__author__ = 'zaleslaw'

import tweepy
from pymongo import MongoClient
import json
from tweepy.utils import import_simplejson



# Put here your Twitter's application keys
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''

# Put here name of MongoDB collection to save dumped tweets (database name is predefined)
TWITTER_TAGS_COLLECTION = ''

# Put here tags to search in Twitter stream
TAGS = ['']

# Change host and port of your Mongo instance database if it is required
MONGO_PORT = 27017
MONGO_HOST = 'localhost'



class StreamToMongoListener(tweepy.StreamListener):
    collection = None
    json = import_simplejson()

    def __init__(self, collection):
        tweepy.StreamListener.__init__(self)
        self.collection = collection

    def on_status(self, tweet):
        print (tweet)

    def on_error(self, status_code):
        print (status_code)
        return False

    def on_data(self, data):
        if data[0].isdigit():
            pass
        else:
            self.collection.insert(json.loads(data))
            print(json.loads(data))

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

client = MongoClient(MONGO_HOST, MONGO_PORT)
db = client['tweets']
tweet_collection = db[TWITTER_TAGS_COLLECTION]


l = StreamToMongoListener(tweet_collection)
streamer = tweepy.Stream(auth=auth, listener=l)
streamer.filter(track = TAGS)






