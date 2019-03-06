from django.test import Client, TestCase
from pvlib import atmosphere
import numpy as np
import pandas as pd

ZDATA = '''{
    "2019-01-01T09:00:00-0800": {"apparent_zenith": "75.64949399351546"},
    "2019-01-01T12:00:00-0800": {"apparent_zenith": "60.93578142843924"}
}'''
AM_DATA = {
    "model": "kastenyoung1989",
    "zenith_data": ZDATA
}


class AtmospherTestCase(TestCase):
    def test_airmass_calc_get(self):
        r = self.client.get('/api/v1/pvlib/airmass/', AM_DATA)
        self.assertEqual(r.status_code, 200)
        s = pd.Series(r.json())
        t = pd.DatetimeIndex(s.index)
        zdata = pd.read_json(ZDATA).T
        times = pd.DatetimeIndex(zdata.index)
        am = atmosphere.get_relative_airmass(
            zdata['apparent_zenith'], AM_DATA['model'])
        assert np.allclose(
            times.values.astype(int), t.values.astype(int))
        assert np.allclose(am, s)

    def test_airmass_calc_post(self):
        r = self.client.post('/api/v1/pvlib/airmass/', AM_DATA)
        self.assertEqual(r.status_code, 200)
        s = pd.Series(r.json())
        t = pd.DatetimeIndex(s.index)
        zdata = pd.read_json(ZDATA).T
        times = pd.DatetimeIndex(zdata.index)
        am = atmosphere.get_relative_airmass(
            zdata['apparent_zenith'], AM_DATA['model'])
        assert np.allclose(
            times.values.astype(int), t.values.astype(int))
        assert np.allclose(am, s)

    def test_airmass_errors(self):
        r = self.client.get('/api/v1/pvlib/airmass/', data={})
        self.assertEqual(r.status_code, 400)
        r = self.client.post('/api/v1/pvlib/airmass/', data={})
        self.assertEqual(r.status_code, 400)
        r = self.client.get(
            '/api/v1/pvlib/airmass/', data={'zenith_data': '{"bad": "data"}'})
        self.assertEqual(r.status_code, 400)
        r = self.client.post(
            '/api/v1/pvlib/airmass/', data={'zenith_data': '{"bad": "data"}'})
        self.assertEqual(r.status_code, 400)

    def test_airmass_defaults_get(self):
        am_data = {'zenith_data': AM_DATA['zenith_data']}
        r = self.client.get('/api/v1/pvlib/airmass/', am_data)
        self.assertEqual(r.status_code, 200)
        s = pd.Series(r.json())
        t = pd.DatetimeIndex(s.index)
        zdata = pd.read_json(ZDATA).T
        times = pd.DatetimeIndex(zdata.index)
        am = atmosphere.get_relative_airmass(zdata['apparent_zenith'])
        assert np.allclose(
            times.values.astype(int), t.values.astype(int))
        assert np.allclose(am, s)

    def test_airmass_default_post(self):
        am_data = {'zenith_data': AM_DATA['zenith_data']}
        r = self.client.post('/api/v1/pvlib/airmass/', am_data)
        self.assertEqual(r.status_code, 200)
        s = pd.Series(r.json())
        t = pd.DatetimeIndex(s.index)
        zdata = pd.read_json(ZDATA).T
        times = pd.DatetimeIndex(zdata.index)
        am = atmosphere.get_relative_airmass(zdata['apparent_zenith'])
        assert np.allclose(
            times.values.astype(int), t.values.astype(int))
        assert np.allclose(am, s)
