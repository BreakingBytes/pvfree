from django.contrib import admin
from parameters.models import PVInverter, PVModule, CEC_Module
from past.builtins import xrange


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
        return tuple(
            [('-999', 'Missing')] +
            [(str(x), '%d - %d [V]' % ((x - self._incr + 1), x))
             for x in xrange(self._incr, self._stop + self._incr, self._incr)])

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
        return (('-999', 'Missing'),
                ('1', '< 1 [kW]'),
                ('2', '1 - 2 [kW]'),
                ('3', '2 - 3 [kW]'),
                ('4', '3 - 4 [kW]'),
                ('5', '4 - 5 [kW]'),
                ('6', '5 - 6 [kW]'),
                ('7', '6 - 7 [kW]'),
                ('8', '7 - 8 [kW]'),
                ('9', '8 - 9 [kW]'),
                ('10', '9 - 10 [kW]'),
                ('20', '10 - 20 [kW]'),
                ('30', '20 - 30 [kW]'),
                ('40', '30 - 40 [kW]'),
                ('50', '40 - 50 [kW]'),
                ('60', '50 - 60 [kW]'),
                ('70', '60 - 70 [kW]'),
                ('80', '70 - 80 [kW]'),
                ('90', '80 - 90 [kW]'),
                ('100', '90 - 100 [kW]'),
                ('200', '100 - 200 [kW]'),
                ('300', '200 - 300 [kW]'),
                ('400', '300 - 400 [kW]'),
                ('500', '400 - 500 [kW]'),
                ('600', '500 - 600 [kW]'),
                ('700', '600 - 700 [kW]'),
                ('800', '700 - 800 [kW]'),
                ('900', '800 - 900 [kW]'),
                ('1000', '900 [kW] - 1 [MW]'),
                ('+1000', '> 1 [MW]'))

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
            return queryset.filter(Paco__gt=float(self.value()) * 1000)
        elif float(self.value()) > 100:
            return queryset.filter(Paco__gt=((float(self.value()) - 100) * 1000),
                                   Paco__lte=float(self.value()) * 1000)
        elif float(self.value()) > 10:
            return queryset.filter(Paco__gt=((float(self.value()) - 10) * 1000),
                                   Paco__lte=float(self.value()) * 1000)
        else:
            return queryset.filter(Paco__gt=((float(self.value()) - 1) * 1000),
                                   Paco__lte=float(self.value()) * 1000)


class PVInverterAdmin(admin.ModelAdmin):
    list_display = (
        'Name', 'Source', 'Manufacturer', 'Vintage',
        'Vac', 'Paco', 'Vdco', 'Pdco', 'Pso', 'C0', 'C1', 'C2', 'C3',
        'Vdcmax', 'Idcmax', 'Mppt_low', 'Mppt_high', 'Pnt'
    )
    list_filter = (VacRangeFilter, PacoRangeFilter)
    fields = ('Name',
              ('Vac', 'Paco'),
              ('Vdco', 'Pdco'), 
              ('C0', 'C1'),
              ('C2', 'C3'),
              ('Pso', 'Pnt'),
              ('Vdcmax', 'Idcmax'),
              ('Mppt_low', 'Mppt_high'))



# Register your models here.
admin.site.register(PVInverter, PVInverterAdmin)
admin.site.register(PVModule)
admin.site.register(CEC_Module)
