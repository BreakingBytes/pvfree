from django.shortcuts import render
from parameters.models import PVInverter, PVModule


def home(request):
    return render(request, 'index.html', {'path': request.path})


def pvinverters(request):
    return render(request, 'pvinverters.html',
        {'path': request.path, 'pvinv_set': PVInverter.objects.values()})


def pvmodules(request):
    return render(request, 'pvmodules.html',
        {'path': request.path, 'pvmod_set': PVModule.objects.values()})
