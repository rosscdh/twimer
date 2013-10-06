from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from views import UserEditView


urlpatterns = patterns('',
    url(r'^latest/$', TemplateView.as_view(template_name='wasted/latest_list.html'), name="latest"),
    url(r'^(?P<pk>.+)/edit/$', login_required(UserEditView.as_view()), name="edit"),
)
