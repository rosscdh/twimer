from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from views import WasterListView


urlpatterns = patterns('',
    url(r'^$', WasterListView.as_view(), name="index"),
)
