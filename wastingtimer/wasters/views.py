# -*- coding: UTF-8 -*-
from django.views.generic import ListView

from django.contrib.auth import get_user_model
from social_auth.db.django_models import UserSocialAuth

User = get_user_model()


class WasterListView(ListView):
    model = User
    queryset = User.objects.prefetch_related('_profile_cache').filter(pk__in=UserSocialAuth.objects.all().values('user_id')).order_by('username')
    template_name = 'wasters/user_list.html'

