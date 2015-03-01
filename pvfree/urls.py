from django.conf.urls import patterns, include, url
from parameters.models import PVInverterResource
from django.contrib import admin

admin.autodiscover()

pvinverter_resource = PVInverterResource()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'pvfree.views.home', name='home'),
    url(r'^api/', include(pvinverter_resource.urls)),
    url(r'^admin/', include(admin.site.urls)),
)