# -*- coding: UTF-8 -*-
import os
from django.conf import settings

from tasks import process_twitter_tweet
from models import TwitterSince
from models import TWEET_TYPES

import tweepy
import datetime
import django_rq
import pdb

CONSUMER_KEY = getattr(settings, 'MINUTESWASTEDAPP_TWITTER_CONSUMER_KEY', os.environ.get('MINUTESWASTEDAPP_TWITTER_CONSUMER_KEY', None))
CONSUMER_SECRET = getattr(settings, 'MINUTESWASTEDAPP_TWITTER_CONSUMER_SECRET', os.environ.get('MINUTESWASTEDAPP_TWITTER_CONSUMER_SECRET', None))

ACCESS_TOKEN = getattr(settings, 'MINUTESWASTEDAPP_TWITTER_ACCESS_TOKEN', os.environ.get('MINUTESWASTEDAPP_TWITTER_ACCESS_TOKEN', None))
ACCESS_TOKEN_SECRET = getattr(settings, 'MINUTESWASTEDAPP_TWITTER_ACCESS_TOKEN_SECRET', os.environ.get('MINUTESWASTEDAPP_TWITTER_ACCESS_TOKEN_SECRET', None))

assert CONSUMER_KEY is not None, 'You must define a MINUTESWASTEDAPP_TWITTER_CONSUMER_KEY in settings or your os.environ'
assert CONSUMER_SECRET is not None, 'You must define a MINUTESWASTEDAPP_CONSUMER_SECRET in settings or your os.environ'
assert ACCESS_TOKEN is not None, 'You must define a MINUTESWASTEDAPP_ACCESS_TOKEN in settings or your os.environ'
assert ACCESS_TOKEN_SECRET is not None, 'You must define a MINUTESWASTEDAPP_ACCESS_TOKEN_SECRET in settings or your os.environ'

TWITTER_AUTH = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
TWITTER_AUTH.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


class AcquireTweets(object):
    """ Base class for collecting & processing tweets """
    since_id = None
    tweet_type = None
    tweets = []

    def __init__(self, **kwargs):
        self.hours_ago = kwargs.pop('hours_ago', 5)

        # Get the since_id from the db
        # @TODO turn into a service (as it will also come from redis)
        try:
            since = TwitterSince.objects.get(since_type=self.tweet_type)
            self.since_id = since.since_id
            # override with custom
            custom_since_id = kwargs.pop('since_id', None)
            if custom_since_id:
                self.since_id
        except TwitterSince.DoesNotExist:
            self.since_id = None

        # get authenticated access to api
        self.api = tweepy.API(TWITTER_AUTH)

    def query_twitter(self):
        raise Exception('Needs to be implemented in calling class')

    def record_since_id(self):
        if self.tweets and type(self.tweets) is tweepy.models.ResultSet:
            # the list provided the most recent tweet is first
            last_tweet = self.tweets[0]
            try:
                TwitterSince.objects.get(since_type=self.tweet_type)
            except TwitterSince.DoesNotExist:
                TwitterSince.objects.create(since_type=self.tweet_type, since_id=0)
            TwitterSince.objects.filter(since_type=self.tweet_type).update(since_id=last_tweet.id)

    def process(self, **kwargs):
        self.tweets = kwargs.pop('tweets', self.query_twitter())
        for tweet in self.tweets:
            try:
                process_twitter_tweet.delay(tweet=tweet, type_of_tweet=self.tweet_type)
            except:
                process_twitter_tweet(tweet=tweet, type_of_tweet=self.tweet_type)
        self.record_since_id()


class MentionsService(AcquireTweets):
    """ Collect and process mentions """
    tweet_type = TWEET_TYPES.mention
    def query_twitter(self):
        return self.api.mentions_timeline(since_id=self.since_id)


class DirectMessagesService(AcquireTweets):
    """ Collect and direct messages """
    tweet_type = TWEET_TYPES.dm
    def query_twitter(self):
        return self.api.direct_messages(since_id=self.since_id)


class FollowerSyncService(AcquireTweets):
    """ create a friendship with people that tweet at us 
    @TODO from this service we woudl call tasks to send marketing info """
    follower = None
    def __init__(self, **kwargs):
        self.follower = kwargs.pop('follower', None)
        super(FollowerSyncService, self).__init__(**kwargs)

    def query_twitter(self):
        if self.follower is not None:
            return self.api.create_friendship(self.follower.id)

    def process(self, **kwargs):
        self.query_twitter()