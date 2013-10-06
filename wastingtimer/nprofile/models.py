# -*- coding: UTF-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from jsonfield import JSONField

PLACEHOLDER_IMAGE = "%simages/placeholder.png"%settings.STATIC_URL


class UserProfile(models.Model):
  user = models.OneToOneField(User, related_name='_profile_cache')
  twitter_image = models.CharField(max_length=255)
  profile_image = models.ImageField(upload_to='profile',blank=True,null=True)
  twitter_data = JSONField(default={})

  def __unicode__(self):
    return u'%s' % self.user.username

  @property
  def location(self):
    return u'%s' % self.twitter_data.get('location', None)

  def image_or_placeholder(self):
    return self.twitter_data.get('profile_image_url', PLACEHOLDER_IMAGE)


# import signals
from signals import create_profile
