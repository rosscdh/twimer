# -*- coding: UTF-8 -*-
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify

from models import Wasted
from wastingtimer.utils import unslugify


def update_total_time(instance):
    timedelta_total_secs = instance.extract_time()
    Wasted.objects.filter(pk=instance.pk).update(timedelta_total_secs=timedelta_total_secs)


@receiver(post_save, sender=Wasted, dispatch_uid='wasted.extract_tags')
def extract_tags(sender, instance, created, **kwargs):
    if created is True:
        # unsligify a list of has_tags so that taggit converts them
        # to internal tags and we also capture the "Beautiful name"
        hashtags = instance.hashtags
        if hashtags:
            tags = unslugify(*hashtags)
            if type(tags) is list:
                instance.tags.add(*tags)
            else:
                instance.tags.add(tags)
        # Update the total_time
        update_total_time(instance=instance)
