from django.db import models, IntegrityError
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
    vintage = models.DateField(default=date(1999, 1, 1))
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
        """
        Class method for creating and updating records from file.

        :param filename: Name of file.
        :param sheet: Name of sheet (None).
        :param mapping: Map of worksheet headers to model fields.
        :type mapping: dict
        """
        # load workbook
        wb = load_workbook(filename, use_iterators = True)
        # use first sheet by default
        if not sheet:
            sheet = wb.get_sheet_names()[0]
        # load worksheet
        ws = wb.get_sheet_by_name(sheet)
        rows = ws.iter_rows()  # row iterator
        # get headers
        headers = [row.value for row in rows.next() if row.value in mapping]
        # check headers match mapping
        if len(headers) < len(mapping):
            raise ValidationError('There are missing or incorrect headers.')
        # iterate over all rows
        for row in rows:
            # using Python-2.6 - doesn't have dictionary comprehension
            # zip will limit size to smaller list, ie: headers
            kwargs = dict([(mapping[h], r.value) for h, r in zip(headers, row)
                           if r.value])
            # convert vintage to date
            if 'vintage' in kwargs:
                kwargs['vintage'] = date(kwargs['vintage'], 1, 1)
            # ducktype temperature range for floats, pop otherwise
            should_be_floats = ('Tamb_low', 'Tamb_max', 'weight', 'Pnt')
            for val in should_be_floats:
                if val in kwargs:
                    try:
                        float(kwargs[val])
                    except ValueError:
                        kwargs.pop(val)
                        # TODO: put these in a "notes" catchall field
            try:
                # create new PVInverter record
                pvinv, created = cls.objects.get_or_create(**kwargs)
            except (IntegrityError, ValidationError) as err:
                # get key of existing record
                vintage = kwargs.get('vintage', date(1999, 1, 1))
                Vaco = kwargs.get('Vaco', -999)
                if cls.objects.filter(manufacturer=kwargs['manufacturer'],
                                      name=kwargs['name'], Vaco=Vaco,
                                      vintage=vintage).exists():
                    if Vaco != -999:
                        kwargs.pop('Vaco')
                    if vintage != date(1999, 1, 1):
                        kwargs.pop('vintage')
                    pvinv = cls.objects.get(
                        manufacturer=kwargs.pop('manufacturer'),
                        name=kwargs.pop('name'),Vaco=Vaco, vintage=vintage)
                    # update existing record
                    for k, v in kwargs.iteritems():
                        setattr(pvinv, k, v)
                    pvinv.save()
                    created = True
                else:
                    raise err  # raise caught exception
            if created:
                # TODO: use logger
                print 'created or updated %s' % pvinv
            else:
                print '%s already exists' % pvinv
            created = False


class PVInverterResource(ModelResource):
    class Meta:
        queryset = PVInverter.objects.all()


