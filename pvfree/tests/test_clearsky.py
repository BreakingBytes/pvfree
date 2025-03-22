from django.test import Client, TestCase
from pvlib import clearsky
import numpy as np
import pandas as pd


class TLTestCase(TestCase):
    def test_tl_lookup(self):
        data={
            'tl_lat': 38.2,
            'tl_lon': -122.1,
            'tl_freq': 'T',
            'tl_tz': -8,
            'tl_start': '2018-01-01 07:00',
            'tl_end': '2018-01-01 08:00'
        }
        r = self.client.get('/api/v1/pvlib/linke-turbidity/', data)
        self.assertEqual(r.status_code, 200)
        s = pd.Series(r.json())
        t = pd.DatetimeIndex(s.index)
        times = pd.date_range(
            start=data['tl_start'], end=data['tl_end'],
            freq=data['tl_freq'], tz='Etc/GMT{:+d}'.format(-data['tl_tz']))
        tl = clearsky.lookup_linke_turbidity(
            times, data['tl_lat'], data['tl_lon'])
        assert np.allclose(
            times.values.astype(int), t.values.astype(int))
        assert np.allclose(tl, s)

    def test_tl_errors(self):
        data={
            'tl_lat': 38.2,
            'tl_lon': -122.1,
            'tl_freq': 'T',
            'tl_tz': -8,
            'tl_start': '2018-1-1 7:00',
            'tl_end': '2018-1-1 8:00'
        }
        r = self.client.get('/api/v1/pvlib/linke-turbidity/', data={})
        self.assertEqual(r.status_code, 400)
        errors = r.json()
        for d in data.keys():
            if d in ('tl_freq', 'tl_tz'):
                continue
            self.assertIn(d, errors)
            self.assertEqual('This field is required.', errors[d][0])
        # check latitude max value
        data['tl_lat'] = 99.9
        r = self.client.get('/api/v1/pvlib/linke-turbidity/', data)
        self.assertEqual(r.status_code, 400)
        errors = r.json()
        self.assertIn('tl_lat', errors)
        self.assertEqual(
            'Ensure this value is less than or equal to 90.', errors['tl_lat'][0])
        # check latitude min value
        data['tl_lat'] = -99.9
        r = self.client.get('/api/v1/pvlib/linke-turbidity/', data)
        self.assertEqual(r.status_code, 400)
        errors = r.json()
        self.assertIn('tl_lat', errors)
        self.assertEqual(
            'Ensure this value is greater than or equal to -90.',
            errors['tl_lat'][0])

    def test_tl_defaults(self):
        data={
            'tl_lat': 38.2,
            'tl_lon': -122.1,
            'tl_freq': 'T',
            'tl_tz': -8,
            'tl_start': '2018-1-1 7:00',
            'tl_end': '2018-1-1 8:00'
        }
        freq = data.pop('tl_freq')
        r = self.client.get('/api/v1/pvlib/linke-turbidity/', data=data)
        self.assertEqual(r.status_code, 200)
        data['tl_freq'] = freq
        tz = data.pop('tl_tz')
        r = self.client.get('/api/v1/pvlib/linke-turbidity/', data=data)
        self.assertEqual(r.status_code, 200)
