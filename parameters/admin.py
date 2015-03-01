from django.contrib import admin
from parameters.models import PVInverter


class PVInverterAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 'source', 'Sandia_ID', 'manufacturer', 'name', 'vintage',
        'Vaco', 'Paco', 'Vdco', 'Pdco', 'Pso', 'C0', 'C1', 'C2', 'C3',
        'Vdcmax', 'Idcmax', 'MPPT_low', 'MPPT_hi', 'Pnt', 'Tamb_low',
        'Tamb_max', 'weight', 'numberMPPTChannels'
    )
    list_filter = ('manufacturer', 'vintage', 'Vaco', 'Paco')
    fields = ('manufacturer',
              ('name', 'vintage'),
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

