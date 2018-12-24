from django.shortcuts import render, get_object_or_404
from parameters.models import PVInverter, PVModule, CEC_Module
from bokeh.plotting import figure
from bokeh.models import Legend, LegendItem
from bokeh.embed import components
from bokeh.palettes import Colorblind5 as cmap
from pvfree.forms import SolarPositionForm
from pvlib.pvsystem import sapm
import numpy as np


def home(request):
    return render(request, 'index.html', {'path': request.path})


def pvinverters(request):
    return render(
        request, 'pvinverters.html',
        {'path': request.path, 'pvinv_set': PVInverter.objects.values()})


def pvmodules(request):
    pvmod_set = PVModule.objects.values()
    for pvmod in pvmod_set:
        pvmod['nameplate'] = PVModule.objects.get(pk=pvmod['id']).nameplate()
    return render(
        request, 'pvmodules.html',
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
    eff = results['p_mp'] / effirrad / pvmod.Area * 100 / 1000
    fig = figure(
        x_axis_label='effective irradiance, Ee [suns]',
        y_axis_label='efficiency [%]',
        title=pvmod.Name,
        plot_width=800, plot_height=600, sizing_mode='scale_width'
    )
    r = fig.multi_line(
        effirrad.tolist(), eff.tolist(), color=cmap, line_width=4)
    legend = Legend(items=[
        LegendItem(label='{:d} [C]'.format(int(ct)), renderers=[r], index=n)
        for n, ct in enumerate(celltemps)])
    fig.add_layout(legend)
    plot_script, plot_div = components(fig)
    return render(
        request, 'pvmodule_detail.html', {
            'path': request.path, 'pvmod': pvmod, 'plot_script': plot_script,
            'plot_div': plot_div, 'pvmod_dict': pvmod_dict})


def cec_modules(request):
    return render(
        request, 'cec_modules.html',
        {'path': request.path, 'cec_mod_set': CEC_Module.objects.values()})


def pvlib(request):
    forms = {}
    if request.method == 'GET':
        forms['solposform'] = SolarPositionForm()
    elif request.method == 'POST':
        forms['solposform'] = SolarPositionForm(request.POST)
    return render(request, 'pvlib.html', {'path': request.path, 'forms': forms})
