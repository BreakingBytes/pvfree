from django.shortcuts import render
from parameters.models import PVInverter


def home(request):
    return render(request, 'index.html', {'path': request.path})


def pvinverters(request):
    pvinv = PVInverter.objects.values()
    context = {'path': request.path, 'pvinverters': pvinv}
    return render(request, 'pvinverters.html', context)

def pvmodules(request):
    return render(request, 'pvmodules.html', {'path': request.path})
