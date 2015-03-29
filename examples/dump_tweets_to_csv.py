# -*- coding: utf-8 -*-

__author__ = 'zaleslaw'

import tweepy
import csv
import codecs
import cStringIO

# Put here your Twitter's application keys
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''

# Put here username of Twitter user whose tweets are interested for you
TWITTER_USER_NAME = ''


class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """

    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")


class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self


class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

api = tweepy.API(auth)

user1 = api.get_user(TWITTER_USER_NAME)


print (user1.screen_name)
print (user1.followers_count)
print (user1.friends_count)

tweets = {}
for tweet in tweepy.Cursor(api.user_timeline).items():
    tweets[str(tweet.created_at)] = tweet.text

print("Number of dumped tweets is " + str(len(tweets)))

with codecs.open('tweets.csv', 'w') as f:
    csvWriter = UnicodeWriter(f, delimiter="|", quoting=csv.QUOTE_NONE, quotechar='')

    for key, value in sorted(tweets.items()):
        try:
            new_value = value.replace(u'\n', u' ')
            csvWriter.writerow([key, new_value])
        except csv.Error as e:
            print ("CSV error({0})".format(e.message))


