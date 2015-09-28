from django.conf.urls import patterns, url
from pexproject.views import *
from django.views.generic.base import RedirectView
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

urlpatterns = patterns('',
    url(r'^$', index, name='index'),
    url(r'^login', login, name='login'),
    url(r'^index', index, name='index'),
    url(r'^searchLoading',searchLoading,name='searchLoading'),
    url(r'^search', search, name='search'),
    url(r'^get_airport', get_airport, name='get_airport'),
    url(r'^getsearchresult', getsearchresult, name='getsearchresult'),
    url(r'^booking', booking, name='booking'),
    
    
#    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes':True}),
)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
