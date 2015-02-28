from django.db import models
from django.core.exceptions import ValidationError
from openpyxl import load_workbook
from datetime import date
from tastypie.resources import ModelResource

MAPPING = {
    "Unique ID#": "Sandia_ID",
    "Manufacturer": "manufacturer",
    "ID": "name",
    "Source": "source",
    "Vintage": "vintage",
    "ac Voltage": "Vaco",
    "Paco": "Paco",
    "Pdco": "Pdco",
    "Vdco": "Vdco",
    "Pso": "Pso",
    "Co": "C0",
    "C1": "C1",
    "C2": "C2",
    "C3": "C3",
    "Vdcmax": "Vdcmax",
    "Idcmax": "Idcmax",
    "MPPT-Low": "MPPT_low",
    "MPPT-Hi": "MPPT_hi",
    "Pnt": "Pnt",
    "Tamb Low": "Tamb_low",
    "Tamb Max": "Tamb_max",
    "Weight": "weight",
    }


# Create your models here.
class PVInverter(models.Model):
    """
    Sandia model PV inverter parameters.
    """
    Sandia_ID = models.IntegerField()
    manufacturer = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    source = models.CharField(max_length=10)
    vintage = models.DateField()
    Paco = models.FloatField(default=-999)
    Vaco = models.FloatField(default=-999)
    Pdco = models.FloatField(default=-999)
    Vdco = models.FloatField(default=-999)
    Pso = models.FloatField(default=-999)
    C0 = models.FloatField(default=-999)
    C1 = models.FloatField(default=-999)
    C2 = models.FloatField(default=-999)
    C3 = models.FloatField(default=-999)
    Vdcmax = models.FloatField(default=-999)
    Idcmax = models.FloatField(default=-999)
    MPPT_low = models.FloatField(default=-999)
    MPPT_hi = models.FloatField(default=-999)
    Pnt = models.FloatField(default=-999)
    Tamb_low = models.FloatField(default=-999)
    Tamb_max = models.FloatField(default=-999)
    weight = models.FloatField(default=-999)
    numberMPPTChannels = models.IntegerField('number of MPPT channels',
                                             default=1)

    def full_name(self):
        return "%s %s (%d) - %d" % (self.manufacturer, self.name, self.Vaco,
                                    self.vintage.year)

    def __unicode__(self):
        return self.full_name()

    class Meta:
        verbose_name = "Inverter"
        unique_together = ('manufacturer', 'name', 'Vaco', 'vintage')

    @classmethod
    def upload(cls, filename, sheet=None, mapping=MAPPING):
        wb = load_workbook(filename, use_iterators = True)
        if not sheet:
            sheet = wb.get_sheet_names()[0]
        ws = wb.get_sheet_by_name(sheet)
        rows = ws.iter_rows()
        headers = [row.value for row in rows.next()]
        if not all(headers):
            raise ValidationError('There is a missing header.')
        if not all(isinstance(h, basestring) for h in headers):
            raise ValidationError('All headers must be strings.')
        for row in rows:
            kwargs = dict([(mapping[h], r.value) for h, r in zip(headers, row) if r.value])
            if 'vintage' in kwargs: kwargs['vintage'] = date(kwargs['vintage'], 1, 1)
            if 'Tamb_low' in kwargs:
                try:
                    Tamb_low = float(kwargs['Tamb_low'])
                except ValueError:
                    kwargs.pop('Tamb_low')
            if 'Tamb_hi' in kwargs:
                try:
                    Tamb_hi = float(kwargs['Tamb_hi'])
                except ValueError:
                    kwargs.pop('Tamb_hi')
            try:
                pvinv, created = cls.objects.get_or_create(**kwargs)
            except ValidationError as err:
                if cls.objects.filter(manufacturer=kwargs['manufacturer'],
                                      name=kwargs['name'],
                                      Vaco=kwargs['Vaco'],
                                      vintage=kwargs['vintage']).exists():
                    pvinv = cls.objects.get(
                        manufacturer=kwargs.pop('manufacturer'),
                        name=kwargs.pop('name'),Vaco=pop('Vaco'),
                        vintage=kwargs.pop('vintage'))
                    for k, v in kwargs.iteritems():
                        setattr(pvinv, k, v)
                    pvinv.save()
                    created = True
                else:
                    raise err
            if created:
                print 'created or updated %s' % pvinv
            created = False


class PVInverterResource(ModelResource):
    class Meta:
        queryset = PVInverter.objects.all()


