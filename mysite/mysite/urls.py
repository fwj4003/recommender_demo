from django.conf.urls import patterns, include, url
from django.contrib import admin
from mysite.view import *
admin.autodiscover()
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^$',homepage),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^show/$',display_meta),
    url(r'^preference/(\d{1})/$',preference),
    url(r'^user_cf/$',user_CF),
    url(r'^item_cf/$',item_CF),
    url(r'^mails/$',SendEmail),
)
