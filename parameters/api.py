from django.contrib.auth.models import User
from parameters.models import PVInverter, PVModule, CEC_Module
from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
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


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        fields = ['email', 'first_name', 'last_name', 'username']
        filtering = {
            'username': ALL,
        }
        allowed_methods = ['get']


class PVInverterResource(ModelResource):
    created_by = fields.ForeignKey(UserResource, 'created_by')
    modified_by = fields.ForeignKey(UserResource, 'modified_by')
    class Meta:
        queryset = PVInverter.objects.all()
        filtering = {
            'created_by': ALL_WITH_RELATIONS,
            "Name": (
                'iexact', 'istartswith', 'icontains', 'iregex', 'iendswith'
            ),
            "Vac": ('exact', 'lt', 'lte', 'gt', 'gte'),
            "Paco": ('exact', 'lt', 'lte', 'gt', 'gte'),
        }
        authorization = IsAuthenticatedOrReadOnly()
        authentication = ApiKeyAuthOrReadOnly()


class PVModuleResource(ModelResource):
    created_by = fields.ForeignKey(UserResource, 'created_by')
    modified_by = fields.ForeignKey(UserResource, 'modified_by')
    class Meta:
        queryset = PVModule.objects.all()
        filtering = {
            'created_by': ALL_WITH_RELATIONS,
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
    created_by = fields.ForeignKey(UserResource, 'created_by')
    modified_by = fields.ForeignKey(UserResource, 'modified_by')
    class Meta:
        queryset = CEC_Module.objects.all()
        filtering = {
            'created_by': ALL_WITH_RELATIONS,
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
