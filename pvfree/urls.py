from django.conf.urls import include, url
from tastypie.api import Api
from parameters.models import (
    PVInverterResource, PVModuleResource, CECModuleResource
)
from pvfree import views as pvfree_views
from parameters import views as param_views
from django.contrib import admin

admin.autodiscover()
v1_api = Api(api_name='v1')
v1_api.register(PVInverterResource())
v1_api.register(PVModuleResource())
v1_api.register(CECModuleResource())

# patterns(prefix, ...) deprecated since django-1.8

urlpatterns = [
    url(r'^$', pvfree_views.home, name='home'),
    url(r'^pvinverters$', pvfree_views.pvinverters, name='pvinverters'),
    url(r'^pvmodules$', pvfree_views.pvmodules, name='pvmodules'),
    url(r'^pvmodules/(?P<pvmodule_id>\d+)/$', pvfree_views.pvmodule_detail,
        name='pvmodule_detail'),
    url(r'^cec_modules$', pvfree_views.cec_modules, name='cec_modules'),
    url(r'^pvlib$', pvfree_views.pvlib, name='pvlib'),
    url(r'^upload$', param_views.file_upload, name='file_upload'),
    url(r'^api/', include(v1_api.urls)),
    url(r'^admin/', include(admin.site.urls)),
]

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# ... the rest of your URLconf goes here ...

urlpatterns += staticfiles_urlpatterns()
