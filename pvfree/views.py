from django.shortcuts import render
from parameters.models import PVInverter


def home(request):
    return render(request, 'index.html', {'path': request.path})


def pvinverters(request):
    pvinv = PVInverter.objects.all()
    return render(request, 'pvinverters.html',
                  {'path': request.path, 'pvinverters': pvinv})

def pvmodules(request):
    return render(request, 'pvmodules.html', {'path': request.path})
