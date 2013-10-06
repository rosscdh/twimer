# -*- coding: UTF-8 -*-
from django import template
from django.utils.safestring import mark_safe
from django.utils import simplejson as json
from wastingtimer.wasted.models import Wasted

register = template.Library()


@register.inclusion_tag('wasted/latest.html')
def latest_tweets(**kwargs):
	max_num = kwargs.get('max', 5)
	return {
		'object_list': Wasted.public.prefetch_related('user', 'user___profile_cache').all().order_by('-id')[:max_num]
	}

@register.filter(is_safe=True, needs_autoescape=True)
def as_json_string(list_or_object, autoescape=None):
    return mark_safe(json.dumps(list_or_object))