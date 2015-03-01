from django.contrib import admin
from parameters.models import PVInverter


class PVInverterAdmin(admin.ModelAdmin):
    list_display = (
        'manufacturer', 'name', 'vintage', 'source', 'Sandia_ID',
        'Vaco', 'Paco', 'Vdco', 'Pdco', 'Pso', 'C0', 'C1', 'C2',
        'C3', 'Vdcmax', 'Idcmax', 'MPPT_low', 'MPPT_hi', 'Pnt',
        'Tamb_low', 'Tamb_max', 'weight', 'numberMPPTChannels'
    )
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

