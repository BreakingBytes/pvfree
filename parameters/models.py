from django.db import models, IntegrityError
from django.core.exceptions import ValidationError
import csv
from datetime import date
from tastypie.resources import ModelResource
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import ApiKeyAuthentication
from django.contrib.auth.models import User
from django.db.models import signals
from tastypie.models import create_api_key
import logging
import re

LOGGER = logging.getLogger(__name__)

signals.post_save.connect(create_api_key, sender=User)


class ApiKeyAuthOrReadOnly(ApiKeyAuthentication):
    def _unauthorized(self):
        return True


class IsAuthenticatedOrReadOnly(DjangoAuthorization):
    def read_list(self, object_list, bundle):
        return object_list

    def read_detail(self, object_list, bundle):
        return True


class PVInverter(models.Model):
    """
    Sandia model PV inverter parameters.
    """
    Name = models.CharField(max_length=100, unique=True)
    Vac = models.FloatField('AC Voltage [V]')
    Paco = models.FloatField('Rated AC power [W]')
    Pdco = models.FloatField('DC power [W]')
    Vdco = models.FloatField('DC voltage [V]')
    Pso = models.FloatField('Self consumption [W]')
    C0 = models.FloatField()
    C1 = models.FloatField()
    C2 = models.FloatField()
    C3 = models.FloatField()
    Pnt = models.FloatField('Nighttime consumption [W]')
    Vdcmax = models.FloatField('Max DC voltage [V]')
    Idcmax = models.FloatField('Max DC current [A]')
    Mppt_low = models.FloatField('Lower bound of MPPT [W]')
    Mppt_high = models.FloatField('Higher bound of MPPT [W]')
    created_on = models.DateField(auto_now_add=True)
    modified_on = models.DateField(auto_now=True)

    def Manufacturer(self):
        mfg, _ = self.Name.split(':', 1)
        return mfg

    def Vintage(self):
        match = re.search('\[(\w*) (\d{4})\]', self.Name)
        yr = date(1900, 1, 1)
        if match:
            src, yr = match.groups()
            try:
                yr = int(yr)
            except ValueError:
                yr = 1900
        return date(yr, 1, 1)

    def Source(self):
        match = re.search('\[(\w*) (\d{4})\]', self.Name)
        if match:
            src, yr = match.groups()
        return src

    def __unicode__(self):
        return self.Name

    class Meta:
        verbose_name = "Inverter"

    @classmethod
    def upload(cls, csv_file='CEC_Inverters.csv'):
        """
        Class method for creating and updating records from file.

        :param csv_file: CSV file
        """
        with open(csv_file, 'rb') as f:
            spamreader = csv.reader(f)
            columns = spamreader.next()
            spamreader.next()
            spamreader.next()
            for spam in spamreader:
                # using Python-2.6 - doesn't have dictionary comprehension
                kwargs = dict(zip(columns, spam))
                try:
                    # create new PVInverter record
                    pvinv, created = cls.objects.get_or_create(**kwargs)
                except (ValueError, IntegrityError, ValidationError) as exc:
                    LOGGER.exception(exc)
                else:
                    if created:
                        LOGGER.info('Created Inverter:\n%r', pvinv)
                    else:
                        LOGGER.warning('Inverter Exists:\n%r', pvinv)


class PVInverterResource(ModelResource):
    class Meta:
        queryset = PVInverter.objects.all()
        filtering = {
            "manufacturer": (
                'iexact', 'istartswith', 'icontains', 'iregex', 'iendswith'
            ),
            "name": (
                'iexact', 'istartswith', 'icontains', 'iregex', 'iendswith'
            ),
            "Vaco": ('exact', 'lt', 'lte', 'gt', 'gte'),
            "vintage": ('year')
        }
        authorization = IsAuthenticatedOrReadOnly()
        authentication = ApiKeyAuthOrReadOnly()


class PVModule(models.Model):
    """
    Sandia model PV module parameters.
    """

    MATERIALS = [
        (1, '2-a-Si'),
        (2, '3-a-Si'),
        (3, 'CIS'),
        (4, 'CdTe'),
        (5, 'EFG'),
        (6, 'GaAs'),
        (7, 'HIT-Si'),
        (8, 'Si-Film'),
        (9, 'a-Si'),
        (10, 'c-Si'),
        (11, 'mc-Si'),
        (12, 'mono-Si')
    ]

    name = models.CharField(max_length=100)
    vintage = models.DateField(default=date(1999, 1, 1))
    vintage_estimated = models.BooleanField(default=False)
    area = models.FloatField(default=-999)
    material = models.IntegerField(choices=MATERIALS, default=10)
    cells_in_series = models.IntegerField(default=-999)
    parallel_strings = models.IntegerField(default=-999)
    fd = models.FloatField('diffuse fraction', default=-999)
    isc0 = models.FloatField(default=-999)
    voc0 = models.FloatField(default=-999)
    imp0 = models.FloatField(default=-999)
    vmp0 = models.FloatField(default=-999)
    ix0 = models.FloatField(default=-999)
    ixx0 = models.FloatField(default=-999)
    c0 = models.FloatField(default=-999)
    c1 = models.FloatField(default=-999)
    c2 = models.FloatField(default=-999)
    c3 = models.FloatField(default=-999)
    c4 = models.FloatField(default=-999)
    c5 = models.FloatField(default=-999)
    c6 = models.FloatField(default=-999)
    c7 = models.FloatField(default=-999)
    aisc = models.FloatField(default=-999)
    aimp = models.FloatField(default=-999)
    bvoc0 = models.FloatField(default=-999)
    mbvoc = models.FloatField(default=-999)
    bvmp0 = models.FloatField(default=-999)
    mbvmp = models.FloatField(default=-999)
    n = models.FloatField('ideality', default=-999)
    a0 = models.FloatField(default=-999)
    a1 = models.FloatField(default=-999)
    a2 = models.FloatField(default=-999)
    a3 = models.FloatField(default=-999)
    a4 = models.FloatField(default=-999)
    b0 = models.FloatField(default=-999)
    b1 = models.FloatField(default=-999)
    b2 = models.FloatField(default=-999)
    b3 = models.FloatField(default=-999)
    b4 = models.FloatField(default=-999)
    b5 = models.FloatField(default=-999)
    dt = models.FloatField(default=-999)
    a = models.FloatField('natural convection', default=-999)
    b = models.FloatField('forced convection', default=-999)
    notes = models.CharField(max_length=100)

    def nameplate(self):
        return self.imp0 * self.vmp0

    def fill_factor(self):
        return self.nameplate() / self.isc0 / self.voc0

    def module_eff(self):
        return self.nameplate() / self.area / 1000.0

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Module"
        unique_together = ('name', 'vintage', 'vintage_estimated', 'notes')


class PVModuleResource(ModelResource):
    class Meta:
        queryset = PVModule.objects.all()
        filtering = {
            "name": (
                'iexact', 'istartswith', 'icontains', 'iregex', 'iendswith'
            ),
            "nameplate": ('exact', 'lt', 'lte', 'gt', 'gte'),
            "vintage": ('year')
        }
        authorization = IsAuthenticatedOrReadOnly()
        authentication = ApiKeyAuthOrReadOnly()
