import os
from datetime import date
from parameters.models import PVModule
from django.test import TestCase, Client
from django.contrib.auth.models import User
import pandas as pd

BASEDIR = os.path.dirname(__file__)
TESTDIR = os.path.join(BASEDIR, 'data')
SANDIA_MODULES = os.path.join(TESTDIR, 'sandia_modules.csv')


class UploadTestCase(TestCase):
    def setUp(self):
        self.testuser = User.objects.create_superuser(
            'testuser', 'user@test.com', '@Test123')

    def test_pvinverter_upload(self):
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
                vintage = '1900'
            is_vintage_estimated = vintage.endswith('(E)')
            if is_vintage_estimated:
                vintage = vintage[:-4]
            vintage = date(int(vintage), 1, 1)
            pvmod = pvmods.filter(Name=row.Name, Vintage=vintage, Notes=row.Notes)
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
