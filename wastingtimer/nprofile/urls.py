from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from views import ProfileView, WastageView


urlpatterns = patterns('',
    url(r'^(?P<slug>.+)/profile/$', login_required(ProfileView.as_view()), name="profile"),
    url(r'^(?P<slug>.+)/wastage/$', login_required(WastageView.as_view()), name="wastage"),
    url(r'^dashboard/$', TemplateView.as_view(template_name='nprofile/dashboard.html'), name="dashboard"),
)
