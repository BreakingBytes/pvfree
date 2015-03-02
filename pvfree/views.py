from django.shortcuts import render
from parameters.models import PVInverter


def home(request):
    return render(request, 'index.html', context={'path': request.path})


def pvinverters(request):
    pvinv_set = PVInverter.objects.all()
    return render(request, 'pvinverters.html',
                  context={'path': request.path, 'pvinverters': pvinv_set})

