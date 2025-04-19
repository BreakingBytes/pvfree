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

    def dehydrate_Material(self, bundle):
        celltype = bundle.data['Material']
        # TODO: use dictionary instead of list
        return PVModule.MATERIALS[celltype][1]


class CECModuleResource(ModelResource):
    class Meta:
        queryset = CEC_Module.objects.all()
        filtering = {
            "Name": (
                'iexact', 'istartswith', 'icontains', 'iregex', 'iendswith'
            ),
            "V_oc_ref": ('exact', 'lt', 'lte', 'gt', 'gte'),
            "I_sc_ref": ('exact', 'lt', 'lte', 'gt', 'gte'),
            "STC": ('exact', 'lt', 'lte', 'gt', 'gte'),
        }
        max_limit = None
        authorization = IsAuthenticatedOrReadOnly()
        authentication = ApiKeyAuthOrReadOnly()

    def dehydrate_Technology(self, bundle):
        cec_mod_tech = bundle.data['Technology']
        # TODO: use dictionary instead of list
        return CEC_Module.TECH[cec_mod_tech][1]

    def dehydrate_Version(self, bundle):
        cec_mod_ver = bundle.data['Version']
        # TODO: use dictionary instead of list
        return CEC_Module.VERSION[cec_mod_ver][1]
