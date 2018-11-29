"""pvlib api"""

from pvlib import solarposition
from django.http import JsonResponse
from django.shortcuts import Http404
import datetime
import pandas as pd


def solarposition_resource(request):
    if request.method == 'GET':
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')
        start = request.GET.get('start')
        end = request.GET.get('end')
        tz = request.GET.get('tz', 0)
        freq = request.GET.get('freq')
        #altiude = request.GET.get('altitude')
        #method = request.GET.get('method')
    else:
        raise Http404('Bad Request')
    # TODO: use forms and validators
    try:
        lat = float(lat)
    except (TypeError, ValueError):
        raise Http404('Bad latitude')
    try:
        lon = float(lon)
    except (TypeError, ValueError):
        raise Http404('Bad longitude')
    try:
        start = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S')
    except (TypeError, ValueError):
        raise Http404('Bad start time')
    try:
        end = datetime.datetime.strptime(end, '%Y-%m-%dT%H:%M:%S')
    except (TypeError, ValueError):
        raise Http404('Bad end time')
    try:
        tz = int(tz)
    except (TypeError, ValueError):
        raise Http404('Bad timezone')
    tz = 'Etc/GMT{:+d}'.format(-tz)
    times = pd.DatetimeIndex(start=start, end=end, freq=freq, tz=tz)
    solpos = solarposition.get_solarposition(times, lat, lon)
    solpos.index = times.strftime('%Y-%m-%dT%H:%M:%S%z')
    # [t.isoformat() for t in times.to_pydatetime()]
    data = solpos.to_dict('index')
    return JsonResponse(data)
