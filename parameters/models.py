import csv
from datetime import date, datetime
from io import StringIO
import logging
import re
from django.db import models, IntegrityError, DataError
from django.core.exceptions import ValidationError, MultipleObjectsReturned
from django.contrib.auth.models import User
from django.db.models import signals
from tastypie.models import create_api_key
import numpy as np

LOGGER = logging.getLogger(__name__)

# auto-create API keys
signals.post_save.connect(create_api_key, sender=User)

MISSING_VINTAGE = 1990


class PVBaseModel(models.Model):
    created_on = models.DateField(auto_now_add=True)
    modified_on = models.DateField(auto_now=True)
    created_by = models.ForeignKey(
        User, related_name='+', on_delete=models.PROTECT)
    modified_by = models.ForeignKey(
        User, related_name='+', on_delete=models.PROTECT)

    class Meta:
        abstract = True


def _upload_csv(csv_file, field_map=None):
    csv_file.seek(0)
    csv_file = StringIO(csv_file.read().decode('utf-8'), newline='')
    spamreader = csv.reader(csv_file)
    columns = next(spamreader)
    if field_map is not None:
        for f, m in field_map.items():
            try:
                columns[columns.index(f)] = m
            except ValueError as exc:
                LOGGER.exception(exc)
                LOGGER.error('field %s is not in columns', f)
            LOGGER.debug('replaced %s with %s', f, m)
    next(spamreader)
    next(spamreader)
    return columns, spamreader


def _upload_helper(cls, kwargs, user, handler=None):
    kwargs['created_by'] = user
    kwargs['modified_by'] = user
    if handler is not None:
        kwargs = handler(cls, kwargs)
        _upload_helper(cls, kwargs, user)
    try:
        # create new PVInverter record
        obj, created = cls.objects.get_or_create(**kwargs)
    except IntegrityError as exc:
        LOGGER.exception(exc)
        LOGGER.error('%s Upload Failed:\n%r', cls.__name__, kwargs)
    except ValueError as exc:
        LOGGER.exception(exc)
        LOGGER.error('%s Upload Failed:\n%r', cls.__name__, kwargs)
    except (ValidationError, MultipleObjectsReturned, DataError) as exc:
        LOGGER.exception(exc)
        LOGGER.error('%s Upload Failed:\n%r', cls.__name__, kwargs)
    else:
        if created:
            LOGGER.info('%s Created:\n%r', cls.__name__, obj)
        else:
            LOGGER.warning('%s Already Exists:\n%r', cls.__name__, obj)


class PVInverter(PVBaseModel):
    """
    Sandia model PV inverter parameters.
    """
    SAM_VERSION = [
        (0, ''), (1, '2018.11.11.r2'), (2, '2018.11.11.r3-r4'),
        (3, '2020.2.29_Release-r1.ssc.238'),
        (4, '2020.2.29.r2.ssc.240-r3.ssc.242'),
        (5, '2020.11.29.r0.ssc.250-2021.12.02.r0.ssc.267'),
        (6, '2021.12.02.r1.ssc.268'), (7, '2021.12.02.r2.ssc.274'),
        (8, '2022.11.21.r0.ssc.278-r3.ssc.280'),
        (9, '2023.12.17.r0.ssc.288-r2.ssc.292'), (10, '2024.12.12.r0.ssc.298')
    ]
    SAMVER_TYPES = {name: idx for idx, name in SAM_VERSION}

    Name = models.CharField(max_length=100)
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
    CEC_Date = models.DateField(default=datetime(MISSING_VINTAGE, 1, 1))
    CEC_Type = models.CharField(max_length=25, blank=True)
    SAM_Version = models.IntegerField(
        choices=SAM_VERSION, default=0, blank=True)


    def Manufacturer(self):
        mfg, _ = self.Name.split(':', 1)
        return mfg

    def Vintage(self):
        if (self.CEC_Date.toordinal()
            != date(MISSING_VINTAGE, 1, 1).toordinal()):
            return self.CEC_Date
        match = re.search(r'\[(\w*) (\d{4})\]', self.Name)
        if match:
            _, yr = match.groups()
            try:
                yr = int(yr)
            except ValueError:
                yr = MISSING_VINTAGE
        else:
            yr = MISSING_VINTAGE
        return date(yr, 1, 1)

    def Source(self):
        if (self.CEC_Date.toordinal()
            != date(MISSING_VINTAGE, 1, 1).toordinal()):
            return 'CEC'
        match = re.search(r'\[(\w*) (\d{4})\]', self.Name)
        src = "UNK"
        if match:
            src, _ = match.groups()
        return src

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name = "Inverter"
        unique_together = ('Name', 'SAM_Version')

    @classmethod
    def upload(cls, csv_file, user, sam_version):
        columns, spamreader = _upload_csv(csv_file)
        for spam in spamreader:
            kwargs = dict(zip(columns, spam))
            # skip blank lines
            if not kwargs:
                continue
            cec_date = kwargs.get('CEC_Date')
            if cec_date is not None:
                try:
                    cec_date = datetime.strptime(cec_date, '%m/%d/%Y')
                except ValueError as exc:
                    if cec_date != 'n/a':
                        LOGGER.exception(exc)
                        LOGGER.error(
                            'CEC_Date: %s has unexpected format', cec_date)
                    cec_date = date(MISSING_VINTAGE, 1, 1)
                    LOGGER.warning('CEC_Date set to default: %s', cec_date)
                kwargs['CEC_Date'] = cec_date
            kwargs['SAM_Version'] = sam_version
            _upload_helper(cls, kwargs, user)


class PVModule(PVBaseModel):
    """
    Sandia model PV module parameters.
    """
    MATERIALS = [
        (0, ''),
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
    TECH_DICT = dict(MATERIALS)
    CELL_TYPES = {name: idx for idx, name in MATERIALS}
    FIELD_MAP = {
        'a': 'A', 'b': 'B', 'dT': 'DTC',
        'Cells in Series': 'Cells_in_Series',
        'Parallel Strings': 'Parallel_Strings'}
    NAN_FIELDS = ('C4', 'C5', 'C6', 'C7', 'IXO', 'IXXO')

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
    Notes = models.TextField(max_length=100)
    is_vintage_estimated = models.BooleanField(default=False)

    def celltype(self):
        return self.TECH_DICT[self.Material]

    def nameplate(self):
        return self.Impo * self.Vmpo

    def fill_factor(self):
        return self.nameplate() / self.Isco / self.Voco

    def module_eff(self):
        return self.nameplate() / self.Area / 1000.0

    def noct(self):
        pvmod_temp = 800.0 * np.exp(self.A + self.B*1.0) + 20.0
        return pvmod_temp + 0.8*self.DTC

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name = "Module"
        unique_together = ('Name', 'Vintage', 'Notes')

    @classmethod
    def upload(cls, csv_file, user):
        columns, spamreader = _upload_csv(csv_file, cls.FIELD_MAP)
        for spam in spamreader:
            kwargs = dict(zip(columns, spam))
            # skip blank lines
            if not kwargs:
                continue
            for f in cls.NAN_FIELDS:
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
                yr = MISSING_VINTAGE
            kwargs['Vintage'] = date(yr, 1, 1)
            LOGGER.debug('year = %d', yr)
            celltype = cls.CELL_TYPES.get(kwargs['Material'], 0)
            kwargs['Material'] = celltype
            LOGGER.debug('cell type = %d', celltype)
            _upload_helper(cls, kwargs, user)


class CEC_Module(PVBaseModel):
    """
    CEC module parameters for DeSoto 1-diode model.
    """
    VERSION = [
        (0, ''), (1, 'MM105'), (2, 'MM106'), (3, 'MM107'), (4, 'NRELv1'),
        (5, 'SAM 2018.9.27'), (6, 'SAM 2018.10.29'), (7, 'SAM 2018.11.11'),
        (8, 'SAM 2018.11.11 r2'), (9, 'SAM 2019.12.19'),
        (10, 'SAM 2020.2.29 r3'), (11, 'SAM 2021.12.02'),
        (12, 'SAM 2023.10.31'), (13, 'SAM 2023.12.17')
    ]
    TECH = [
        (0, ''),
        (1, '1-a-Si'),
        (2, '2-a-Si'),
        (3, '3-a-Si'),
        (4, 'CIGS'),
        (5, 'CIS'),
        (6, 'CdTe'),
        (7, 'HIT-Si'),
        (8, 'Mono-c-Si'),
        (9, 'Multi-c-Si'),
        (10, 'Thin Film'),
        (11, 'a-Si'),
        (12, 'a-Si/nc')
    ]
    VER_TYPES = {name: idx for idx, name in VERSION}
    TECH_TYPES = {name: idx for idx, name in TECH}

    Name = models.CharField(max_length=100)
    BIPV = models.BooleanField()
    Date = models.DateField()
    T_NOCT = models.FloatField()
    A_c = models.FloatField()
    N_s = models.IntegerField()
    I_sc_ref = models.FloatField()
    V_oc_ref = models.FloatField()
    I_mp_ref = models.FloatField()
    V_mp_ref = models.FloatField()
    alpha_sc = models.FloatField()
    beta_oc = models.FloatField()
    a_ref = models.FloatField()
    I_L_ref = models.FloatField()
    I_o_ref = models.FloatField()
    R_s = models.FloatField()
    R_sh_ref = models.FloatField()
    Adjust = models.FloatField()
    gamma_r = models.FloatField()
    Version = models.IntegerField(choices=VERSION, default=0, blank=True)
    PTC = models.FloatField()
    Technology = models.IntegerField(choices=TECH)
    Bifacial = models.BooleanField(default=0)
    STC = models.FloatField()
    Length = models.FloatField(blank=True, null=True)
    Width = models.FloatField(blank=True, null=True)

    def nameplate(self):
        return self.I_mp_ref * self.V_mp_ref

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name = "CEC Module"
        unique_together = ('Name', 'Date', 'Version')

    @classmethod
    def upload(cls, csv_file, user):
        columns, spamreader = _upload_csv(csv_file)
        for spam in spamreader:
            kwargs = dict(zip(columns, spam))
            # skip blank lines
            if not kwargs:
                continue
            _upload_helper(cls, kwargs, user, upload_handler)

    @classmethod
    def upload_handler(cls, kwargs):
        # handle technology
        tech = cls.TECH_TYPES.get(kwargs['Technology'], 0)
        kwargs['Technology'] = tech
        LOGGER.debug('Technology = %d', tech)
        # handle version
        ver = cls.VER_TYPES.get(kwargs['Version'], 0)
        kwargs['Version'] = ver
        LOGGER.debug('Version = %d', ver)
        # handle BIPV
        bipv = kwargs['BIPV'] == 'Y'
        kwargs['BIPV'] = bipv
        LOGGER.debug('BIPV = %r', bipv)
        # handle date
        timestamp = kwargs['Date']
        try:
            timestamp = datetime.strptime(timestamp, '%m/%d/%Y')
        except (ValueError, TypeError) as exc:
            LOGGER.exception(exc)
            timestamp = datetime.now()
        kwargs['Date'] = timestamp
        LOGGER.debug('Date = %s', timestamp.isoformat())
        # handle Length and Width
        if not kwargs['Length']:
            kwargs['Length'] = None
        if not kwargs['Width']:
            kwargs['Width'] = None
        return kwargs