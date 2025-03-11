"""pvlib api"""

from pvlib import solarposition, clearsky, atmosphere, iotools
from django.http import JsonResponse
from django.shortcuts import Http404
from django.views.decorators.csrf import csrf_exempt
import datetime
import pandas as pd
from pvfree.forms import (
    SolarPositionForm, LinkeTurbidityForm, AirmassForm, WeatherForm)
import json
import calendar
from requests.exceptions import HTTPError


def solarposition_resource(request):
    if request.method == 'GET':
        params = SolarPositionForm(request.GET)
    else:
        params = SolarPositionForm(request.POST)
    if params.is_valid():
        lat = params.cleaned_data['lat']
        lon = params.cleaned_data['lon']
        start = params.cleaned_data['start']
        end = params.cleaned_data['end']
        tz = params.cleaned_data['tz']
        freq = params.cleaned_data['freq']
    else:
        return JsonResponse(params.errors, status=400)
    tz = tz or 0  # if tz is None then use zero
    freq = freq or 'H'  # if freq if '' then use 'H'
    if start > end:
        return JsonResponse(
            {'start': ['End time must be after start.']}, status=400)
    # drop the timezone
    start = start.replace(tzinfo=None)
    end = end.replace(tzinfo=None)
    tz = 'Etc/GMT{:+d}'.format(-tz)
    try:
        times = pd.date_range(start=start, end=end, freq=freq, tz=tz)
    except ValueError as exc:
        return JsonResponse({'freq': [str(exc)]}, status=400)
    # FIXME: *** Shift time to middle of intervals! ***
    solpos = solarposition.get_solarposition(times, lat, lon)
    solpos.index = times.strftime('%Y-%m-%dT%H:%M:%S%z')
    data = solpos.to_dict('index')
    return JsonResponse(data)


def linke_turbidity_resource(request):
    if request.method == 'GET':
        params = LinkeTurbidityForm(request.GET)
    else:
        params = LinkeTurbidityForm(request.POST)
    if params.is_valid():
        lat = params.cleaned_data['tl_lat']
        lon = params.cleaned_data['tl_lon']
        start = params.cleaned_data['tl_start']
        end = params.cleaned_data['tl_end']
        tz = params.cleaned_data['tl_tz']
        freq = params.cleaned_data['tl_freq']
    else:
        return JsonResponse(params.errors, status=400)
    tz = tz or 0  # if tz is None then use zero
    freq = freq or 'H'  # if freq if '' then use 'H'
    if start > end:
        return JsonResponse(
            {'start': ['End time must be after start.']}, status=400)
    # drop the timezone
    start = start.replace(tzinfo=None)
    end = end.replace(tzinfo=None)
    tz = 'Etc/GMT{:+d}'.format(-tz)
    try:
        times = pd.date_range(start=start, end=end, freq=freq, tz=tz)
    except ValueError as exc:
        return JsonResponse({'freq': [str(exc)]}, status=400)
    tl = clearsky.lookup_linke_turbidity(times, lat, lon)
    tl.index = times.strftime('%Y-%m-%dT%H:%M:%S%z')
    data = tl.to_dict()
    return JsonResponse(data)


APPARENT_OR_TRUE = dict([
    ('simple', 'apparent_zenith'), ('kasten1966', 'apparent_zenith'),
    ('youngirvine1967', 'zenith'),
    ('kastenyoung1989', 'apparent_zenith'),
    ('gueymard1993', 'apparent_zenith'), ('young1994', 'zenith'),
    ('pickering2002', 'apparent_zenith')
])


@csrf_exempt
def airmass_resource(request):
    if request.method == 'GET':
        params = AirmassForm(request.GET)
    else:
        params = AirmassForm(request.POST)
    if params.is_valid():
        zenith_data = params.cleaned_data['zenith_data']
        zenith_file = params.cleaned_data['zenith_file']
        filetype = params.cleaned_data['filetype']
        model = params.cleaned_data['model']
    else:
        return JsonResponse(params.errors, status=400)
    if filetype is None:
        filetype = 'json'
    if zenith_data is None and zenith_file is None:
        return JsonResponse(params.errors, status=400)
    if zenith_data:
        zenith_data = json.loads(zenith_data)
        if len(zenith_data) == 0:
            return JsonResponse(
                {"zenith_data": ["Invalid data in zenith data."]}, status=400)
        times = pd.DatetimeIndex(zenith_data.keys())  # keys not necessary
        columns = {}
        for row in zenith_data.values():
            if not columns:
                columns = {k: [float(v)] for k, v in row.items()}
            else:
                for k, v in row.items():
                    columns[k].append(float(v))
        zenith_data = pd.DataFrame(columns, index=times)
    if zenith_file and zenith_data is None:
        if filetype == 'json':
            zenith_data = pd.read_json(zenith_file)
        elif filetype == 'csv':
            zenith_data = pd.read_csv(zenith_file)
        elif filetype == 'xlsx':
            zenith_data = pd.read_excel(zenith_file)
        else:
            return JsonResponse(params.errors, status=400)
    if model is None:
        model = 'kastenyoung1989'
    try:
        apparent_or_true = APPARENT_OR_TRUE[model]
    except KeyError:
        return JsonResponse(params.errors, status=400)
    am = atmosphere.get_relative_airmass(zenith_data[apparent_or_true], model)
    am.fillna(-9999.9, inplace=True)
    am.index = times.strftime('%Y-%m-%dT%H:%M:%S%z')
    data = am.to_dict()
    return JsonResponse(data)


@csrf_exempt
def weather_resource(request):
    if request.method == 'GET':
        params = WeatherForm(request.GET)
    else:
        params = WeatherForm(request.POST)
    if params.is_valid():
        tmy_lat = params.cleaned_data['tmy_lat']
        tmy_lon = params.cleaned_data['tmy_lon']
        tmy_year_name = params.cleaned_data['tmy_year_name']
        tmy_coerced_year = params.cleaned_data['tmy_coerced_year']
        tmy_freq = params.cleaned_data['tmy_freq']
        tmy_source = params.cleaned_data['tmy_source']
        tmy = params.cleaned_data['tmy']
        tmy_nrel_key = params.cleaned_data['tmy_nrel_key']
        tmy_email = params.cleaned_data['tmy_email']
        tmy_file = params.cleaned_data['tmy_file']
    else:
        return JsonResponse(params.errors, status=400)
    if tmy_nrel_key is None:
        tmy_nrel_key = "DEMO_KEY"
    if tmy:
        start_year = tmy_coerced_year or 1990
    else:
        start_year = tmy_year_name
    # PSM3
    if tmy_source.lower() == "psm3":
        if tmy:
            tmy_name = 'tmy'
            tmy_freq = 60
            times = pd.date_range(
                start=f'{start_year}-01-01 00:30',
                end=f'{start_year}-12-31 23:59:59',
                freq='H')
        else:
            tmy_freq = int(tmy_freq)
            tmy_name = str(tmy_year_name)
            start_time = f'00:{tmy_freq//2:02d}:{int((tmy_freq%2)/2*60):02d}'
            times = pd.date_range(
                start=f'{start_year}-01-01 {start_time}',
                end=f'{start_year}-12-31 23:59:59',
                freq=f'{tmy_freq}T')
        try:
            tmy_data, metadata = iotools.get_psm3(
                latitude=tmy_lat, longitude=tmy_lon, api_key=tmy_nrel_key,
                email=tmy_email, names=tmy_name, interval=tmy_freq)
        except Exception as exc:
            # could be either HTTPError or ReadTimeout 
            return JsonResponse({'psm3': exc.args[0]}, status=400)
        if calendar.isleap(int(start_year)):
            feb29 = (times.month==2) & (times.day==29)
            times = times[~feb29]
        tmy_tz = metadata['Time Zone']
        times = times.tz_localize(f'Etc/GMT{-tmy_tz:+d}')
        tmy_data.index = times.strftime('%Y-%m-%dT%H:%M:%S%z')
        # DROP_COLS = ['Year', 'Month', 'Day', 'Hour', '']
        # tmy_data = tmy_data.drop(columns=DROP_COLS)
        # TODO: do better with columns
        DATA_COLS = ['GHI', 'DHI', 'DNI', 'Temperature', "Wind Speed"]
        data = tmy_data[DATA_COLS].to_dict('index')
        # TODO: also return metadata like city, state, timezone, etc
    return JsonResponse(data)
