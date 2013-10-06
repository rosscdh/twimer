# -*- coding: UTF-8 -*-
from django.db import models
from django.db.models import Count

from wastingtimer.utils import TWEET_TYPES


class WastedManager(models.Manager):
    def by_tag(self, user, **filters):
        tags = {}
        items = self.get_query_set().filter(user=user, **filters)

        for w in items:
            minutes = w.extract_time()
            # for each tag in the hashtags
            for t in w.hashtags:
                # init the tag value if its not in our list of tags
                if t not in tags:
                    tags[t] = 0
                tags[t] += minutes

        return tags


class WastedPublicManager(WastedManager):
    def get_query_set(self):
        return super(WastedManager, self).get_query_set().filter(tweet_type=TWEET_TYPES.mention)


class WastedPrivateManager(WastedManager):
    def get_query_set(self):
        return super(WastedManager, self).get_query_set().filter(tweet_type=TWEET_TYPES.dm)


class WastedUserManager(WastedManager):
    def by_user(self, user):
        if user.is_staff:
            return super(WastedUserManager, self).get_query_set().filter()
        else:
            return super(WastedUserManager, self).get_query_set().filter(user=user)