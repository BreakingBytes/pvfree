from django.shortcuts import render
from parameters.models import PVInverter
from django.http import HttpResponse


def home(request):
    return render(request, 'index.html', {'path': request.path})


def pvinverters(request):
    pvinv_set = PVInverter.objects.all()
    return render(request, 'pvinverters.html',
                  {'path': request.path, 'pvinverters': pvinv_set})

def pvmodules(request):
    return HttpResponse('welcome to pvmodules page.')