import os
from datetime import date, datetime
from parameters.models import PVModule, PVInverter, CEC_Module, MISSING_VINTAGE
from django.test import TestCase, Client
from django.contrib.auth.models import User
import pandas as pd

BASEDIR = os.path.dirname(__file__)
TESTDIR = os.path.join(BASEDIR, 'data')
SANDIA_MODULES = os.path.join(TESTDIR, 'sandia_modules.csv')
CEC_INVERTERS = os.path.join(TESTDIR, 'cec_inverters.csv')
CEC_MODULES = os.path.join(TESTDIR, 'cec_modules.csv')
PVINV_SAM_VERSIONS = {k: v for v, k in PVInverter.SAM_VERSION}
PVINV_SAM_VERSION = PVINV_SAM_VERSIONS['2018.11.11.r2']  # 1
PVINV_CEC_DATE = date(int(MISSING_VINTAGE), 1, 1)
PVINV_CEC_TYPE = ''


class UploadTestCase(TestCase):
    def setUp(self):
        self.testuser = User.objects.create_superuser(
            'testuser', 'user@test.com', '@Test123')

    def test_cecmodule_upload(self):
        self.client.force_login(self.testuser)
        with open(CEC_MODULES) as fp:
            payload = {'uploadSelect': 'CEC Modules', 'uploadFile': fp}
            r = self.client.post('/upload/', payload)
        self.assertEqual(r.status_code, 302)
        cecmods = CEC_Module.objects.all()
        expected = pd.read_csv(CEC_MODULES, skiprows=[1, 2])
        for row in expected.itertuples():
            timestamp = datetime.strptime(row.Date, '%m/%d/%Y')
            sam_version = CEC_Module.VER_TYPES[row.Version]
            cecmod = cecmods.filter(
                Name=row.Name, Date=timestamp, Version=sam_version)
            self.assertEqual(len(cecmod), 1)
            cecmod = cecmod[0]
            for col in expected.columns:
                cecmod_val = getattr(cecmod, col)
                val = getattr(row, col)
                if col in ('Name', 'Version', 'Date'):
                    continue
                elif col == 'Technology':
                    self.assertEqual(cecmod.get_Technology_display(), val)
                elif col == 'BIPV':
                    self.assertEqual(cecmod_val, val == 'Y')
                elif col in ('N_s', 'Bifacial'):
                    self.assertEqual(cecmod_val, val)
                else:
                    self.assertAlmostEqual(cecmod_val, val)
            

    def test_pvinverter_upload(self):
        self.client.force_login(self.testuser)
        with open(CEC_INVERTERS) as fp:
            payload = {
                'uploadSelect': 'CEC Inverters',
                'samVersionSelect': PVINV_SAM_VERSION,
                'uploadFile': fp}
            r = self.client.post('/upload/', payload)
        self.assertEqual(r.status_code, 302)
        pvinvs = PVInverter.objects.all()
        expected = pd.read_csv(CEC_INVERTERS, skiprows=[1, 2])
        expected['CEC_Date'] = PVINV_CEC_DATE
        expected['CEC_Type'] = PVINV_CEC_TYPE
        for row in expected.itertuples():
            pvinv = pvinvs.filter(Name=row.Name, SAM_Version=1)
            self.assertEqual(len(pvinv), 1)
            pvinv = pvinv[0]
            for col in expected.columns:
                pvinv_val = getattr(pvinv, col)
                val = getattr(row, col)
                if col in ('Name', 'SAM_Version'):
                    continue
                elif col == 'CEC_Date':
                    self.assertEqual(pvinv_val, val)
                else:
                    self.assertAlmostEqual(pvinv_val, val)


    def test_sandia_module_update(self):
        self.client.force_login(self.testuser)
        with open(SANDIA_MODULES) as fp:
            payload = {
                'uploadSelect': 'Sandia Modules', 'uploadFile': fp}
            r = self.client.post('/upload/', payload)
        self.assertEqual(r.status_code, 302)
        pvmods = PVModule.objects.all()
        expected = pd.read_csv(SANDIA_MODULES, skiprows=[1, 2])
        for row in expected.itertuples():
            vintage = row.Vintage
            if not vintage:
                vintage = MISSING_VINTAGE
            is_vintage_estimated = vintage.endswith('(E)')
            if is_vintage_estimated:
                vintage = vintage[:-4]
            vintage = date(int(vintage), 1, 1)
            pvmod = pvmods.filter(
                Name=row.Name, Vintage=vintage, Notes=row.Notes)
            self.assertEqual(len(pvmod), 1)
            pvmod = pvmod[0]
            self.assertEqual(is_vintage_estimated, pvmod.is_vintage_estimated)
            for col in expected.columns:
                if col in ('Name', 'Vintage', 'Notes'):
                    continue
                elif col == 'Cells in Series':
                    val = row[5]
                elif col == 'Parallel Strings':
                    val = row[6]
                else:
                    val = getattr(row, col)
                fn = PVModule.FIELD_MAP.get(col, col)
                pvmod_val = getattr(pvmod, fn)
                if col in ('Material',):
                    self.assertEqual(pvmod_val, PVModule.CELL_TYPES[val])
                elif col in PVModule.NAN_FIELDS:
                    if not val:
                        self.assertIsNone(pvmod_val)
                else:
                    self.assertAlmostEqual(pvmod_val, val)
