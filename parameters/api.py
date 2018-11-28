from parameters.models import PVInverter, PVModule, CEC_Module
from tastypie.resources import ModelResource
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import ApiKeyAuthentication


class ApiKeyAuthOrReadOnly(ApiKeyAuthentication):
    def _unauthorized(self):
        return True


class IsAuthenticatedOrReadOnly(DjangoAuthorization):
    def read_list(self, object_list, bundle):
        return object_list

    def read_detail(self, object_list, bundle):
        return True


class PVInverterResource(ModelResource):
    class Meta:
        queryset = PVInverter.objects.all()
        filtering = {
            "Name": (
                'iexact', 'istartswith', 'icontains', 'iregex', 'iendswith'
            ),
            "Vac": ('exact', 'lt', 'lte', 'gt', 'gte'),
            "Paco": ('exact', 'lt', 'lte', 'gt', 'gte'),
        }
        authorization = IsAuthenticatedOrReadOnly()
        authentication = ApiKeyAuthOrReadOnly()


class PVModuleResource(ModelResource):
    class Meta:
        queryset = PVModule.objects.all()
        filtering = {
            "Name": (
                'iexact', 'istartswith', 'icontains', 'iregex', 'iendswith'
            ),
            "nameplate": ('exact', 'lt', 'lte', 'gt', 'gte'),
            "Vintage": ('year')
        }
        authorization = IsAuthenticatedOrReadOnly()
        authentication = ApiKeyAuthOrReadOnly()


class CECModuleResource(ModelResource):
    class Meta:
        queryset = CEC_Module.objects.all()
        filtering = {
            "Name": (
                'iexact', 'istartswith', 'icontains', 'iregex', 'iendswith'
            ),
            "V_oc_ref": ('exact', 'lt', 'lte', 'gt', 'gte'),
            "I_sc_ref": ('exact', 'lt', 'lte', 'gt', 'gte'),
        }
        authorization = IsAuthenticatedOrReadOnly()
        authentication = ApiKeyAuthOrReadOnly()
