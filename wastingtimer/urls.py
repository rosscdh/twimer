from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^auth/', include('social_auth.urls')),
    url(r'^wasters/', include('wastingtimer.wasters.urls', namespace='wasters')),
	url(r'^', include('wastingtimer.wasted.urls', namespace='wasted')),
    url(r'^', include('wastingtimer.nprofile.urls', namespace='nprofile')),
    url(r'^', include('wastingtimer.theme.urls', namespace='theme')),
)
