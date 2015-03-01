from django.contrib import admin
from parameters.models import PVInverter


class VacoRangeFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Vaco'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'Vaco'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        _incr = 100
        _stop = 1000
        return tuple(
            [('-999', 'Missing')] +
            [(str(x), '%d - %d' % ((x - _incr + 1), x))
             for x in xrange(_incr, _stop + _incr, _incr)])

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
            return queryset.filter(Vaco=float(self.value()))                
        else:
            return queryset.filter(Vaco__gt=(float(self.value()) - 100),
                                   Vaco__lte=float(self.value()))


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
        _incr = 100
        _stop = 1000
        return tuple(
            [('-999', 'Missing')] +
            [(str(x), '%d - %d' % ((x - _incr + 1), x))
             for x in xrange(_incr, _stop + _incr, _incr)])

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
        else:
            return queryset.filter(Paco__gt=(float(self.value()) - 100),
                                   Paco__lte=float(self.value()))


class PVInverterAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 'source', 'Sandia_ID', 'manufacturer', 'name', 'vintage',
        'Vaco', 'Paco', 'Vdco', 'Pdco', 'Pso', 'C0', 'C1', 'C2', 'C3',
        'Vdcmax', 'Idcmax', 'MPPT_low', 'MPPT_hi', 'Pnt', 'Tamb_low',
        'Tamb_max', 'weight', 'numberMPPTChannels'
    )
    list_filter = (VacoRangeFilter, PacoRangeFilter, 'vintage', 'manufacturer')
    fields = (('manufacturer', 'name'), 'vintage',
              ('Sandia_ID', 'source'),
              ('Vaco', 'Paco'),
              ('Vdco', 'Pdco'), 
              ('C0', 'C1'),
              ('C2', 'C3'),
              ('Pso', 'Pnt'),
              ('Vdcmax', 'Idcmax'),
              ('MPPT_low', 'MPPT_hi'),
              ('Tamb_low', 'Tamb_max'),
              ('weight', 'numberMPPTChannels'))



# Register your models here.
admin.site.register(PVInverter, PVInverterAdmin)

