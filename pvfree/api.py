"""pvlib api"""

from pvlib import solarposition
from pvlib import clearsky
from django.http import JsonResponse
from django.shortcuts import Http404
import datetime
import pandas as pd
from pvfree.forms import SolarPositionForm, LinkeTurbidityForm


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
    tl = clearsky.lookup_linke_turbidity(times, lat, lon)
    tl.index = times.strftime('%Y-%m-%dT%H:%M:%S%z')
    # [t.isoformat() for t in times.to_pydatetime()]
    data = tl.to_dict()
    return JsonResponse(data)