from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings 

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysy.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^polls/', include('polls.urls', namespace="polls")),
    url(r'^admin/', include(admin.site.urls)),
#    url(r'^admin/', include(admin.site.register)),
)

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG is False:   #if DEBUG is True it will be served automatically 
    urlpatterns += patterns('', 
            url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}), 
    )
