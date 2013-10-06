# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.encoding import smart_unicode

from taggit.managers import TaggableManager
from jsonfield import JSONField

from wastingtimer.utils import TWEET_TYPES, get_namedtuple_choices
from managers import WastedManager, WastedPublicManager, WastedPrivateManager, WastedUserManager

import re

User = get_user_model()


class Wasted(models.Model):
    """ Model for wasted time tweets 
    stores the tweets
    """
    user = models.ForeignKey(User)
    timedelta_total_secs = models.FloatField(null=True,)
    tweet = models.CharField(max_length=255, null=True)
    twitter_id = models.BigIntegerField(db_index=True)
    tweet_type = models.IntegerField(choices=TWEET_TYPES.get_choices(), db_index=True)
    tweet_data = JSONField(default={})
    created_at = models.DateTimeField(auto_now=False, auto_now_add=False, db_index=True)

    tags = TaggableManager()

    objects = WastedManager()
    public = WastedPublicManager()
    private = WastedPrivateManager()
    user_objects = WastedUserManager()

    def __unicode__(self):
        return u'%s - %s' % (self.text, self.created_at,)

    @property
    def is_private(self):
        """ Direct Messages are regarded as
        private tweets
        """
        return self.tweet_type == TWEET_TYPES.dm

    @property
    def text(self):
        """ Extract the tweet.text from the saved tweet json object 
        store as property for easy reference
        """
        text = self.tweet if self.tweet else self.tweet_data.get('text', None)
        if text:
            text = re.sub(r'\@minutes_wasted', '',text)
        return u'%s' % smart_unicode(text if text else u'No Tweet Text Found')

    @property
    def geo(self):
        return self.tweet_data.get('geo', None)

    @property
    def source(self):
        return self.tweet_data.get('source', None)

    @property
    def hashtags(self):
        """ Extract the inbuilt twitter hashtag for use as categories 
        """
        tags = []
        try:
            tags = [t.name for t in self.tags.all()]
            tags[0]
        except:
            if self.tweet_data and 'entities' in self.tweet_data:
                tags = [unicode(i['text']).lower() for i in self.tweet_data['entities'].get('hashtags', [])]
        return tags

    def extract_hashtags(self,text=None):
        text = text if text is not None else self.text
        return re.findall(r'(#\w+)', text)

    def extract_time(self):
        """ Extract the proposed wasted time 
        27min 2hrs etc.. try to make it as inclusive as possible
        datetime libs
        """
        hours,minutes = 0,0
        find = re.search(ur"(\d+:\d+)", self.text, re.UNICODE)
        if find:
            hours,minutes = find.group(0).split(":")
        return (int(hours)*60) + int(minutes)


class TwitterSince(models.Model):
    """ Model for saving the since_id of the
    last imported tweet """
    since_id = models.BigIntegerField()
    since_type = models.IntegerField(choices=TWEET_TYPES.get_choices(), unique=True, db_index=True)

# Must be defined in models.py and at the end of the file so it auto loads
from signals import extract_tags