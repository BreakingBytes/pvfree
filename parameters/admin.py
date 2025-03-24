from django.contrib import admin
from parameters.models import PVInverter, PVModule, CEC_Module
from past.builtins import xrange
from itertools import chain


class VacRangeFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Vac'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'Vac'

    _incr = 100
    _stop = 1000

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return [('-999', 'Missing')] + [
            (str(x), '%d - %d [V]' % ((x - self._incr + 1), x))
            for x in xrange(self._incr, self._stop + self._incr, self._incr)
        ] + [('+1000', '> 1000 [V]')]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if not self.value():
            return
        elif self.value() == '-999':
            return queryset.filter(Vac=float(self.value()))
        elif self.value() == '+1000':
            return queryset.filter(Vac__gt=float(self.value()))
        else:
            return queryset.filter(Vac__gt=(float(self.value()) - self._incr),
                                   Vac__lte=float(self.value()))


class PacoRangeFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Paco'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'Paco'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return [('-999', 'Missing')] + [
            (str(z), '{:d} - {:d} [kW]'.format(z-10**(len(str(z-1))-1), z))
            for z in chain(*[[x*10**y for x in range(2,11)] for y in range(3)])
        ] + [('+1000', '> 1 [MW]')]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if not self.value():
            return
        elif self.value() == '-999':
            return queryset.filter(Paco=float(self.value()))
        elif self.value() == '+1000':
            return queryset.filter(Paco__gt=float(self.value())*1000)
        elif float(self.value()) > 100:
            return queryset.filter(Paco__gt=((float(self.value()) - 100)*1000),
                                   Paco__lte=float(self.value())*1000)
        elif float(self.value()) > 10:
            return queryset.filter(Paco__gt=((float(self.value()) - 10)*1000),
                                   Paco__lte=float(self.value())*1000)
        else:
            return queryset.filter(Paco__gt=((float(self.value()) - 1)*1000),
                                   Paco__lte=float(self.value())*1000)


class PVInverterAdmin(admin.ModelAdmin):
    list_display = (
        'Name', 'Source', 'Manufacturer', 'Vintage', 'revision',
        'Vac', 'Paco', 'Vdco', 'Pdco', 'Pso', 'C0', 'C1', 'C2', 'C3',
        'Vdcmax', 'Idcmax', 'Mppt_low', 'Mppt_high', 'Pnt', 'CEC_Date',
        'CEC_Type', 'created_on', 'modified_on'
    )
    search_fields = ('Name',)
    list_filter = ('revision', VacRangeFilter, PacoRangeFilter)
    fields = (
        'Name', ('Vac', 'Paco'), ('Vdco', 'Pdco'), ('C0', 'C1'), ('C2', 'C3'),
        ('Pso', 'Pnt'), ('Vdcmax', 'Idcmax'), ('Mppt_low', 'Mppt_high'),
        ('CEC_Date', 'CEC_Type'), ('created_by', 'modified_by'))


class PVModuleAdmin(admin.ModelAdmin):
    list_display = ('Name', 'nameplate', 'Vintage', 'Material',
                    'Isco', 'Voco', 'Impo', 'Vmpo', 'created_on', 'modified_on')
    fields = (
        'Name', ('Vintage', 'is_vintage_estimated'),
        ('Area', 'Material'), ('Cells_in_Series', 'Parallel_Strings'),
        ('Isco', 'Voco'), ('Impo', 'Vmpo'), ('IXO', 'IXXO'),
        ('Aisc', 'Aimp'), ('Bvoco', 'Bvmpo'), ('Mbvoc', 'Mbvmp'),
        ('C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7'),
        ('A0', 'A1', 'A2', 'A3', 'A4'),
        ('B0', 'B1', 'B2', 'B3', 'B4', 'B5'),
        ('N', 'DTC', 'FD'), ('A', 'B'),
        'Notes', ('created_by', 'modified_by')
    )
    search_fields = ('Name',)
    list_filter = ('Material',)


class CEC_ModuleAdmin(admin.ModelAdmin):
    list_display = (
        'Name', 'nameplate', 'Date', 'Technology', 'Version', 'I_sc_ref',
        'V_oc_ref', 'I_mp_ref', 'V_mp_ref', 'created_on', 'modified_on')
    fields = (
        ('Name', 'BIPV'), ('Date', 'Version'), ('Technology', 'Bifacial'),
        ('Length', 'Width'), ('A_c', 'N_s'), ('I_sc_ref', 'V_oc_ref'),
        ('I_mp_ref', 'V_mp_ref'), ('I_L_ref', 'I_o_ref'),
        ('alpha_sc', 'beta_oc'), ('R_s', 'R_sh_ref'), ('a_ref', 'gamma_r'),
        ('Adjust', 'T_NOCT'), ('PTC', 'STC'), ('created_by', 'modified_by')
    )
    search_fields = ('Name',)
    list_filter = ('Technology', 'BIPV', 'Bifacial', 'Version')


# Register your models here.
admin.site.register(PVInverter, PVInverterAdmin)
admin.site.register(PVModule, PVModuleAdmin)
admin.site.register(CEC_Module, CEC_ModuleAdmin)
