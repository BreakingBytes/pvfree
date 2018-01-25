from django.shortcuts import render, get_object_or_404
from parameters.models import PVInverter, PVModule


def home(request):
    return render(request, 'index.html', {'path': request.path})


def pvinverters(request):
    return render(request, 'pvinverters.html',
                  {'path': request.path,
                   'pvinv_set': PVInverter.objects.values()})


def pvmodules(request):
    pvmod_set = PVModule.objects.values()
    for pvmod in pvmod_set:
        pvmod['nameplate'] = PVModule.objects.get(pk=pvmod['id']).nameplate()
    return render(request, 'pvmodules.html',
                  {'path': request.path, 'pvmod_set': pvmod_set})


def pvmodule_detail(request, pvmodule_id):
    pvmod = get_object_or_404(PVModule, pk=pvmodule_id)
    return render(request, 'pvmodule_detail.html',
                  {'path': request.path, 'pvmod': pvmod})


def cec_modules(request):
    return render(request, 'cec_modules.html', {'path': request.path})


def pvlib(request):
    return render(request, 'pvlib.html', {'path': request.path})
