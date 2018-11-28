import matplotlib
matplotlib.use('Agg')
from django.shortcuts import render, get_object_or_404
from parameters.models import PVInverter, PVModule, CEC_Module
import matplotlib.pyplot as plt, mpld3
from pvlib.pvsystem import sapm
import numpy as np


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
    fieldnames = PVModule._meta.get_fields()
    pvmod_dict = {k.name: getattr(pvmod, k.name) for k in fieldnames}
    for k in ['IXO', 'IXXO', 'C4', 'C5', 'C6', 'C7']:
        if pvmod_dict[k] is None:
            pvmod_dict[k] = 0.
    celltemps = np.linspace(0, 100, 5)
    effirrad, celltemp = np.meshgrid(np.linspace(0.1, 1, 10), celltemps)
    results = sapm(effirrad, celltemp, pvmod_dict)
    eff = results['p_mp'] / effirrad / pvmod.Area * 100
    fig = plt.figure(figsize=(8, 6))
    plt.plot(effirrad.T, eff.T)
    plt.grid()
    plt.xlabel('effective irradiance, Ee [suns]')
    plt.ylabel('efficiency [%]')
    plt.title(pvmod.Name)
    plt.legend(celltemps)
    plotdata = mpld3.fig_to_html(fig)
    return render(request, 'pvmodule_detail.html',
                  {'path': request.path, 'pvmod': pvmod, 'plotdata': plotdata})


def cec_modules(request):
    return render(request, 'cec_modules.html',
                  {'path': request.path,
                   'cec_mod_set': CEC_Module.objects.values()})


def pvlib(request):
    return render(request, 'pvlib.html', {'path': request.path})
