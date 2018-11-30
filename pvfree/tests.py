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
            'start': '2018-01-01T07:00:00',
            'end': '2018-01-01T08:00:00'
        }
        r = self.client.get('/api/v1/pvlib/solarposition/', data)
        self.assertEqual(r.status_code, 200)
        s = pd.DataFrame(r.json()).T
        t = pd.DatetimeIndex(s.index)
        times = pd.DatetimeIndex(
            start=data['start'], end=data['end'],
            freq=data['freq'], tz='Etc/GMT{:+d}'.format(-data['tz']))
        solpos = solarposition.get_solarposition(times, data['lat'], data['lon'])
        assert np.allclose(times.values.astype(int),
                           t.values.astype(int))
        assert np.allclose(solpos.apparent_zenith, s.apparent_zenith)
        assert np.allclose(solpos.azimuth, s.azimuth)
