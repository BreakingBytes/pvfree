from django.test import Client, TestCase
from pvlib import solarposition
import numpy as np
import pandas as pd


class SolPosTestCase(TestCase):
    def test_solpos_calc(self):
        data={
            'lat': 38.2,
            'lon': -122.1,
            'freq': 'T',
            'tz': -8,
            'start': '2018-01-01 07:00',
            'end': '2018-01-01 08:00'
        }
        r = self.client.get('/api/v1/pvlib/solarposition/', data)
        self.assertEqual(r.status_code, 200)
        s = pd.DataFrame(r.json()).T
        t = pd.DatetimeIndex(s.index)
        times = pd.DatetimeIndex(
            start=data['start'], end=data['end'],
            freq=data['freq'], tz='Etc/GMT{:+d}'.format(-data['tz']))
        solpos = solarposition.get_solarposition(
            times, data['lat'], data['lon'])
        assert np.allclose(
            times.values.astype(int), t.values.astype(int))
        assert np.allclose(solpos.apparent_zenith, s.apparent_zenith)
        assert np.allclose(solpos.azimuth, s.azimuth)

    def test_solpos_errors(self):
        data={
            'lat': 38.2,
            'lon': -122.1,
            'freq': 'T',
            'tz': -8,
            'start': '2018-1-1 7:00',
            'end': '2018-1-1 8:00'
        }
        r = self.client.get('/api/v1/pvlib/solarposition/', data={})
        self.assertEqual(r.status_code, 400)
        errors = r.json()
        for d in data.keys():
            if d in ('freq', 'tz'):
                continue
            self.assertIn(d, errors)
            self.assertEqual('This field is required.', errors[d][0])
        # check latitude max value
        data['lat'] = 99.9
        r = self.client.get('/api/v1/pvlib/solarposition/', data)
        self.assertEqual(r.status_code, 400)
        errors = r.json()
        self.assertIn('lat', errors)
        self.assertEqual(
            'Ensure this value is less than or equal to 90.', errors['lat'][0])
        # check latitude min value
        data['lat'] = -99.9
        r = self.client.get('/api/v1/pvlib/solarposition/', data)
        self.assertEqual(r.status_code, 400)
        errors = r.json()
        self.assertIn('lat', errors)
        self.assertEqual(
            'Ensure this value is greater than or equal to -90.',
            errors['lat'][0])

    def test_solpos_defaults(self):
        data={
            'lat': 38.2,
            'lon': -122.1,
            'freq': 'T',
            'tz': -8,
            'start': '2018-1-1 7:00',
            'end': '2018-1-1 8:00'
        }
        freq = data.pop('freq')
        r = self.client.get('/api/v1/pvlib/solarposition/', data=data)
        self.assertEqual(r.status_code, 200)
        data['freq'] = freq
        tz = data.pop('tz')
        r = self.client.get('/api/v1/pvlib/solarposition/', data=data)
        self.assertEqual(r.status_code, 200)
