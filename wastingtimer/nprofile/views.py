# -*- coding: UTF-8 -*-
from django.views.generic import DetailView
from django.views.generic import ListView

from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.utils import simplejson as json

from wastingtimer.wasted.models import Wasted

import datetime

User = get_user_model()


class ProfileView(DetailView):
    model = User
    template_name = 'nprofile/profile.html'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset().prefetch_related('_profile_cache')

        slug = self.kwargs.get(self.slug_url_kwarg, None)
        queryset = queryset.filter(**{'username': slug})

        try:
            obj = queryset.get()
        except ObjectDoesNotExist:
            raise Http404(u"No %(verbose_name)s found matching the query" %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj

    def daterange_list(self, **kwargs):
        """ provide a simple interface to the public or private queryset
        as well as a filter foor date_range"""
        public = kwargs.pop('public', True)
        date_of = kwargs.pop('date_of', None)

        if public:
            qs = Wasted.public
        else:
            qs = Wasted.private

        if date_of:
            date_from = datetime.datetime.combine(date_of, datetime.time.min)
            date_to = datetime.datetime.combine(date_of, datetime.time.max)
            return qs.by_tag(user=self.object, created_at__range=(date_from, date_to))
        else:
            return qs.by_tag(user=self.object)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        date_of = request.GET.get('date_of', None)

        if date_of:
            date_of = datetime.datetime.strptime(date_of, "%Y-%m-%d")
            wasted_list = self.daterange_list(public=True, date_of=date_of)
        else:
            wasted_list = self.daterange_list(public=True)

        # Looking at own profile
        if request.user == self.object:
            wasted_list.update(self.daterange_list(public=False, date_of=date_of))

        context.update({
            'date_of': date_of
            ,'wasted_list': json.dumps(wasted_list)
        })
        return self.render_to_response(context)


class WastageView(ListView):
    allow_empty = True
    model = Wasted
    context_object_name = 'object_list'
    
    def get_queryset(self):
        """
        Get the list of items for this view. This must be an iterable, and may
        be a queryset (in which qs-specific behavior will be enabled).
        """
        user = User.objects.get(username=self.kwargs.get('slug'))
        return self.model._default_manager.prefetch_related('user').filter(user=user)