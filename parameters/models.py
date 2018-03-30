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
        src = "UNK"
        if match:
            src, yr = match.groups()
        return src

    def __unicode__(self):
        return self.Name

    class Meta:
        verbose_name = "Inverter"

    @classmethod
    def upload_csv(cls, csv_file='CEC_Inverters.csv'):
        """
        Class method for creating and updating records from file.

        :param csv_file: CSV file
        """
        with open(csv_file, 'rb') as f:
            cls.upload(f)

    @classmethod
    def upload(cls, f):
        if isinstance(f, basestring):
            cls.upload_csv(f)
        spamreader = csv.reader(f)
        columns = spamreader.next()
        spamreader.next()
        spamreader.next()
        for spam in spamreader:
            kwargs = dict(zip(columns, spam))
            try:
                # create new PVInverter record
                pvinv, created = cls.objects.get_or_create(**kwargs)
            except (ValueError, IntegrityError, ValidationError) as exc:
                LOGGER.exception(exc)
                LOGGER.error('Inverter Upload Failed:\n%r', kwargs)
            else:
                if created:
                    LOGGER.info('Created Inverter:\n%r', pvinv)
                else:
                    LOGGER.warning('Inverter Exists:\n%r', pvinv)


class PVInverterResource(ModelResource):
    class Meta:
        queryset = PVInverter.objects.all()
        filtering = {
            "Name": (
                'iexact', 'istartswith', 'icontains', 'iregex', 'iendswith'
            ),
            "Vac": ('exact', 'lt', 'lte', 'gt', 'gte'),
            "Paco": ('exact', 'lt', 'lte', 'gt', 'gte'),
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
        (5, 'EFG mc-Si'),
        (6, 'GaAs'),
        (7, 'HIT-Si'),
        (8, 'Si-Film'),
        (9, 'a-Si / mono-Si'),
        (10, 'c-Si'),
        (11, 'mc-Si')
    ]

    Name = models.CharField(max_length=100)
    Vintage = models.DateField()
    Area = models.FloatField()
    Material = models.IntegerField(choices=MATERIALS)
    Cells_in_Series = models.IntegerField()
    Parallel_Strings = models.IntegerField()
    Isco = models.FloatField('Short Circuit Current [A]')
    Voco = models.FloatField('Open Circuit Voltage [V]')
    Impo = models.FloatField('Max Power Current [A]')
    Vmpo = models.FloatField('Max Power Voltage [V]')
    Aisc = models.FloatField('Short Circuit Current Tempco')
    Aimp = models.FloatField('Max Power Current Tempco')
    C0 = models.FloatField()
    C1 = models.FloatField()
    Bvoco = models.FloatField('Open Circuit Voltage Tempco')
    Mbvoc = models.FloatField()
    Bvmpo = models.FloatField('Max Power Voltage Tempco')
    Mbvmp = models.FloatField()
    N = models.FloatField('Diode Ideality Factor')
    C2 = models.FloatField()
    C3 = models.FloatField()
    A0 = models.FloatField()
    A1 = models.FloatField()
    A2 = models.FloatField()
    A3 = models.FloatField()
    A4 = models.FloatField()
    B0 = models.FloatField()
    B1 = models.FloatField()
    B2 = models.FloatField()
    B3 = models.FloatField()
    B4 = models.FloatField()
    B5 = models.FloatField()
    DTC = models.FloatField('Cell Temp Delta')
    FD = models.FloatField('Diffuse Fraction')
    A = models.FloatField('Natural Convection Coeff')
    B = models.FloatField('Forced Convection Coeff')
    C4 = models.FloatField(null=True, blank=True)
    C5 = models.FloatField(null=True, blank=True)
    IXO = models.FloatField(null=True, blank=True)
    IXXO = models.FloatField(null=True, blank=True)
    C6 = models.FloatField(null=True, blank=True)
    C7 = models.FloatField(null=True, blank=True)
    Notes = models.CharField(max_length=100)
    is_vintage_estimated = models.BooleanField(default=False)

    def nameplate(self):
        return self.Impo * self.Vmpo

    def fill_factor(self):
        return self.nameplate() / self.Isco / self.Voco

    def module_eff(self):
        return self.nameplate() / self.Area / 1000.0

    def __unicode__(self):
        return self.Name

    class Meta:
        verbose_name = "Module"
        unique_together = ('Name', 'Vintage', 'Notes')

    @classmethod
    def upload_csv(cls, csv_file='Sandia_Modules.csv'):
        with open(csv_file, 'rb') as f:
            cls.upload(f)

    @classmethod
    def upload(cls, f):
        if isinstance(f, basestring):
            cls.upload_csv(f)
        # FIXME: be DRY - this is an exact copy of PVInverter.upload()
        field_map = {
            'a': 'A', 'b': 'B', 'dT': 'DTC',
            'Cells in Series': 'Cells_in_Series',
            'Parallel Strings': 'Parallel_Strings'}
        _, celltypes = zip(*cls.MATERIALS)
        nan_fields = ('C4', 'C5', 'C6', 'C7', 'IXO', 'IXXO')
        spamreader = csv.reader(f)
        columns = spamreader.next()
        spamreader.next()
        spamreader.next()
        for f, m in field_map.iteritems():
            columns[columns.index(f)] = m
            LOGGER.debug('replaced %s with %s', f, m)
        for spam in spamreader:
            kwargs = dict(zip(columns, spam))
            for f in nan_fields:
                if not kwargs[f]:
                    nan = kwargs.pop(f)
                    LOGGER.debug('popped "%s" from %s', nan, f)
            yr = kwargs['Vintage']
            if yr.endswith('(E)'):
                yr = yr[:4]
                kwargs['is_vintage_estimated'] = True
            try:
                yr = int(yr)
            except ValueError:
                yr = 1900
            kwargs['Vintage'] = date(yr, 1, 1)
            LOGGER.debug('year = %d', yr)
            celltype = kwargs['Material']
            try:
                celltype = celltypes.index(celltype) + 1
            except IndexError:
                celltype = 10
            kwargs['Material'] = celltype
            LOGGER.debug('cell type = %d', celltype)
            try:
                # create new PVInverter record
                pvmod, created = cls.objects.get_or_create(**kwargs)
            except (ValueError, IntegrityError, ValidationError) as exc:
                LOGGER.exception(exc)
                LOGGER.error('Module Upload Failed:\n%r', kwargs)
            else:
                if created:
                    LOGGER.info('Created Module:\n%r', pvmod)
                else:
                    LOGGER.warning('Module Exists:\n%r', pvmod)


class PVModuleResource(ModelResource):
    class Meta:
        queryset = PVModule.objects.all()
        filtering = {
            "Name": (
                'iexact', 'istartswith', 'icontains', 'iregex', 'iendswith'
            ),
            "nameplate": ('exact', 'lt', 'lte', 'gt', 'gte'),
            "Vintage": ('year')
        }
        authorization = IsAuthenticatedOrReadOnly()
        authentication = ApiKeyAuthOrReadOnly()
