from django.conf.urls import include, url
from tastypie.api import Api
from parameters.models import PVInverterResource, PVModuleResource
from django.contrib import admin

admin.autodiscover()
v1_api = Api(api_name='v1')
v1_api.register(PVInverterResource())
v1_api.register(PVModuleResource())

# patterns(prefix, ...) deprecated since django-1.8

urlpatterns = [
    url(r'^$', 'pvfree.views.home', name='home'),
    url(r'^pvinverters$', 'pvfree.views.pvinverters', name='pvinverters'),
    url(r'^pvmodules$', 'pvfree.views.pvmodules', name='pvmodules'),
    url(r'^cec_modules$', 'pvfree.views.cec_modules', name='cec_modules'),
    url(r'^pvlib$', 'pvfree.views.pvlib', name='pvlib'),
    url(r'^api/', include(v1_api.urls)),
    url(r'^admin/', include(admin.site.urls)),
]

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# ... the rest of your URLconf goes here ...

urlpatterns += staticfiles_urlpatterns()
