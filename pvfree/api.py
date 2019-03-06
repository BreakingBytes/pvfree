"""pvlib api"""

from pvlib import solarposition, clearsky, atmosphere
from django.http import JsonResponse
from django.shortcuts import Http404
from django.views.decorators.csrf import csrf_exempt
import datetime
import pandas as pd
from pvfree.forms import SolarPositionForm, LinkeTurbidityForm, AirmassForm
import json


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
        times = pd.DatetimeIndex(start=start, end=end, freq=freq, tz=tz)
    except ValueError as exc:
        return JsonResponse({'freq': [str(exc)]}, status=400)
    solpos = solarposition.get_solarposition(times, lat, lon)
    solpos.index = times.strftime('%Y-%m-%dT%H:%M:%S%z')
    # [t.isoformat() for t in times.to_pydatetime()]
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
        times = pd.DatetimeIndex(start=start, end=end, freq=freq, tz=tz)
    except ValueError as exc:
        return JsonResponse({'freq': [str(exc)]}, status=400)
    tl = clearsky.lookup_linke_turbidity(times, lat, lon)
    tl.index = times.strftime('%Y-%m-%dT%H:%M:%S%z')
    # [t.isoformat() for t in times.to_pydatetime()]
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
            return JsonResponse({"zenith_data": ["Invalid data in zenith data"]},
            status=400)
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
    if not model:
        model = 'kastenyoung1989'
    apparent_or_true = APPARENT_OR_TRUE.get(model)
    if not apparent_or_true:
        return JsonResponse(params.errors, status=400)
    am = atmosphere.get_relative_airmass(zenith_data[apparent_or_true], model)
    am.fillna(-9999.9, inplace=True)
    am.index = times.strftime('%Y-%m-%dT%H:%M:%S%z')
    data = am.to_dict()
    return JsonResponse(data)
