from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pig_engine.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^request_server$', 'pig_server.views.pig_server_main'),
    url(r'^$', 'mue.views.mueView'),
    url(r'^index.html$', 'mue.views.mueView'),
)
