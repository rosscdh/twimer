# -*- coding: UTF-8 -*-
from django.dispatch import receiver
from django.db.models.signals import post_save

from django.contrib.auth.models import User
from models import UserProfile


@receiver(post_save, sender=User, dispatch_uid='nprofile.create_profile')
def create_profile(sender, instance, created, **kwargs):
    if created is True:
        # create the UserProfile model for this user
        UserProfile.objects.get_or_create(user=instance)        

