from django.db import models
from openpyxl import load_workbook


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
    Paco = models.FloatField()
    Vaco = models.FloatField()
    Pdco = models.FloatField()
    Vdco = models.FloatField()
    Pso = models.FloatField()
    C0 = models.FloatField()
    C1 = models.FloatField()
    C2 = models.FloatField()
    C3 = models.FloatField()
    Vdcmax = models.FloatField()
    Idcmax = models.FloatField()
    MPPT_low = models.FloatField()
    MPPT_hi = models.FloatField()
    Pnt = models.FloatField()
    Tamb_low = models.FloatField()
    Tamb_max = models.FloatField()
    weight = models.FloatField()
    numberMPPTChannels = models.IntegerField('number of MPPT channels',
                                             default=1)

    def full_name(self):
        return "%s %s (%d)" % (self.manufacturer, self.modelName, self.Vaco)

    def __unicode__(self):
        return self.full_name

    class Meta:
        verbose_name = "Inverter"
        unique_together = ('manufacturer', 'modelName', 'Vaco')

    @classmethod
    def upload(cls, filename, sheet=None, mapping=MAPPING):
        wb = load_workbook(filename, use_iterators = True)
        if not sheet:
            sheet = wb.get_sheet_names()[0]
        ws = wb.get_sheet_by_name(sheet)
        rows = ws.iterrows()
        headers = [row.value for row in rows.next()]
        assert(all(headers), 'There is a missing header.')
        assert(all(isinstance(h, basestring) for h in headers),
               'All headers must be strings.')
        for row in rows:
            kwargs = {mapping[h]: r.value for h, r in zip(headers, row)}
            try:
                pvinv, created = cls.objects.get_or_create(**kwargs)
            except ValidationError as err:
                if cls.objects.filter(manufacturer=kwargs['manufacturer'],
                                      name=kwargs['name'],
                                      Vaco=kwargs['Vaco']).exists():
                    pvinv = cls.objects.get(
                        manufacturer=kwargs.pop('manufacturer'),
                        name=kwargs.pop('name'),Vaco=pop('Vaco'))
                    for k, v in kwargs.iteritems():
                        setattr(pvinv, k, v)
                    pvinv.save()
                else:
                    raise err


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
    "MPPT-Low": "MPPT_Low",
    "MPPT-Hi": "MPPT_Hi",
    "Pnt": "Pnt",
    "Tamb Low": "Tamb_low",
    "Tamb Max": "Tamb_max",
    "Weight": "weight",
    }
}
