from django.conf.urls import include, re_path
from tastypie.api import Api
from parameters.api import (
    PVInverterResource, PVModuleResource, CECModuleResource)
from pvfree import views as pvfree_views
from parameters import views as param_views
from django.contrib import admin
from pvfree.api import (
    solarposition_resource, linke_turbidity_resource, airmass_resource,
    weather_resource)

admin.autodiscover()
v1_api = Api(api_name='v1')
v1_api.register(PVInverterResource())
v1_api.register(PVModuleResource())
v1_api.register(CECModuleResource())

# patterns(prefix, ...) deprecated since django-1.8

urlpatterns = [
    re_path(r'^$', pvfree_views.home, name='home'),
    re_path(r'^pvinverters/$', pvfree_views.pvinverters, name='pvinverters'),
    re_path(r'^pvinverters/(?P<pvinverter_id>\d+)/$',
        pvfree_views.pvinverter_detail, name='pvinverter_detail'),
    re_path(r'^sam_versions/$', pvfree_views.sam_versions,
        name='sam_versions'),
    re_path(r'^pvmodules/$', pvfree_views.pvmodules, name='pvmodules'),
    re_path(r'^pvmodules_tech/$', pvfree_views.pvmodules_tech,
        name='pvmodules_tech'),
    re_path(r'^pvmodules/(?P<pvmodule_id>\d+)/$', pvfree_views.pvmodule_detail,
        name='pvmodule_detail'),
    re_path(r'^cec_modules/$', pvfree_views.cec_modules, name='cec_modules'),
    re_path(r'^cec_modules_tech/$', pvfree_views.cec_modules_tech,
        name='cec_modules_tech'),
    re_path(r'^cec_modules/(?P<cec_module_id>\d+)/$',
        pvfree_views.cec_module_detail, name='cec_module_detail'),
    re_path(r'^pvlib/$', pvfree_views.pvlib, name='pvlib'),
    re_path(r'^upload/$', param_views.file_upload, name='file_upload'),
    re_path(r'^api/', include(v1_api.urls)),
    re_path(r'^api/v1/pvlib/weather/$', weather_resource, name='weather'),
    re_path(r'^api/v1/pvlib/solarposition/$', solarposition_resource,
        name='solarposition'),
    re_path(r'^api/v1/pvlib/linke-turbidity/$', linke_turbidity_resource,
        name='linke_turbidity'),
    re_path(r'^api/v1/pvlib/airmass/$', airmass_resource, name='airmass'),
    re_path(r'^admin/', admin.site.urls),
]

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# ... the rest of your URLconf goes here ...

urlpatterns += staticfiles_urlpatterns()
