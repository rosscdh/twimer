from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView


urlpatterns = patterns('',
    url(r'^about-us/$', TemplateView.as_view(template_name='theme/about_us.html'), name="about_us"),
    url(r'^(?P<slug>.+)/profile/$', login_required(TemplateView.as_view(template_name='theme/profile.html')), name="profile"),
    url(r'^$', TemplateView.as_view(template_name='theme/index.html'), name="index"),
)
