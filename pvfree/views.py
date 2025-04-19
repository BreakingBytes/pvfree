from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models.functions import Lower
from parameters.models import PVInverter, PVModule, CEC_Module
from bokeh.plotting import figure
from bokeh.models import Legend, LegendItem
from bokeh.embed import components
from bokeh.palettes import Colorblind5 as cmap
from pvfree.forms import (
    SolarPositionForm, LinkeTurbidityForm, AirmassForm, WeatherForm)
from pvlib.pvsystem import sapm, calcparams_cec, singlediode, inverter
from pvlib.singlediode import bishop88
import numpy as np
import re


def home(request):
    return render(request, 'index.html', {'path': request.path})


def _datatables_helper(post_request):
    columns = []
    order = []
    for k, v in post_request.items():
        if k.startswith('columns'):
            m = re.match('^columns\[(\d+)](.+)$', k)
            col_idx, col_key = m.groups()
            col_idx = int(col_idx)
            try:
                columns[col_idx][col_key] = v
            except IndexError:
                columns.append({col_key: v})
        elif k.startswith('order'):
            m = re.match('^order\[(\d+)](.+)$', k)
            order_idx, order_key = m.groups()
            order_idx = int(order_idx)
            try:
                order[order_idx][order_key] = v
            except IndexError:
                order.append({order_key: v})
    return columns, order


def pvinverters(request):
    # using datatables.net with ajax to return from API
    return render(request, 'pvinverters.html', {'path': request.path})


def pvinverter_detail(request, pvinverter_id):
    pvinv = get_object_or_404(PVInverter, pk=pvinverter_id)
    fieldnames = PVInverter._meta.get_fields()
    pvinv_dict = {k.name: getattr(pvinv, k.name) for k in fieldnames}
    dc_voltages = [pvinv.Mppt_low, pvinv.Vdco, pvinv.Mppt_high]
    pwr_lvl = np.array([0.1, 0.2, 0.3, 0.5, 0.75, 1])
    dc_power = pvinv.Pdco * pwr_lvl
    dc_power, dc_voltage = np.meshgrid(dc_power, dc_voltages)
    pac = inverter.sandia(dc_voltage, dc_power, pvinv_dict)
    eff = pac / dc_power
    eff_disp = 100*eff
    if pvinv.Paco > 1000:
        dc_power_disp = dc_power/1000
        disp_units = 'kW'
    else:
        dc_power_disp = dc_power
        disp_units = 'W'
    fig = figure(
        x_axis_label=f'DC power, Pdc [{disp_units}]',
        y_axis_label='efficiency [%]',
        title=pvinv.Name,
        width=800, height=600, sizing_mode='scale_width')
    r = fig.multi_line(
        dc_power_disp.tolist(), eff_disp.tolist(), color=cmap[:3], line_width=4)
    legend = Legend(items=[
        LegendItem(label='{:d} [V]'.format(int(vdc)), renderers=[r], index=n)
        for n, vdc in enumerate(dc_voltages)])
    fig.add_layout(legend)
    plot_script, plot_div = components(fig)
    return render(
        request, 'pvinverter_detail.html', {
            'path': request.path, 'pvinv': pvinv, 'plot_script': plot_script,
            'plot_div': plot_div, 'pvinv_dict': pvinv_dict})


def sam_versions(request):
    return JsonResponse(dict(PVInverter.SAM_VERSION))


def pvmodules(request):
    pvmod_set = PVModule.objects.values()
    for pvmod in pvmod_set:
        pvmod['nameplate'] = PVModule.objects.get(pk=pvmod['id']).nameplate()
        pvmod['celltype'] = PVModule.objects.get(pk=pvmod['id']).celltype()
    return render(
        request, 'pvmodules.html',
        {'path': request.path, 'pvmod_set': pvmod_set})


def pvmodules_tech(request):
    return JsonResponse(PVModule.TECH_DICT)


def pvmodule_detail(request, pvmodule_id):
    pvmod = get_object_or_404(PVModule, pk=pvmodule_id)
    fieldnames = PVModule._meta.get_fields()
    pvmod_dict = {k.name: getattr(pvmod, k.name) for k in fieldnames}
    for k in ['IXO', 'IXXO', 'C4', 'C5', 'C6', 'C7']:
        if pvmod_dict[k] is None:
            pvmod_dict[k] = 0.
    celltemps = np.linspace(0, 100, 5)  # [C]
    effirrad = np.linspace(100, 1000, 10)  # [W/m2]
    effirrad, celltemp = np.meshgrid(effirrad, celltemps)
    # Ee in [W/m2] pvlib>=0.7, in suns for pvlib<0.7
    results = sapm(effirrad, celltemp, pvmod_dict)
    eff = results['p_mp'] / effirrad / pvmod.Area * 100
    fig = figure(
        x_axis_label='effective irradiance, Ee [W/m' + u"\u00B2" + ']',
        y_axis_label='efficiency [%]',
        title=pvmod.Name,
        width=800, height=600, sizing_mode='scale_width'
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


def _filter_by_technology(search_term):
    search_term = str(search_term).lower()
    search_results = []
    for tech, idx in CEC_Module.TECH_TYPES.items():
        if search_term in tech.lower():
            search_results.append(idx)
    return search_results


@csrf_exempt
def cec_modules(request):
    if request.method == 'GET':
        # using datatables.net with ajax to return values from API
        return render(request, 'cec_modules.html', {'path': request.path})
    elif request.method == 'POST':
        columns, order = _datatables_helper(request.POST)
        draw = int(request.POST.get('draw'))
        start = int(request.POST.get('start'))
        length = int(request.POST.get('length'))
        search_value = request.POST.get('search[value]')
        limit = start+length
        total_records = CEC_Module.objects.count()
        # TODO: sort columns
        if search_value:
            tech_search = _filter_by_technology(search_value)
            cecmod_set = (
                CEC_Module.objects.filter(Name__icontains=search_value)
                | CEC_Module.objects.filter(BIPV__icontains=search_value)
                | CEC_Module.objects.filter(Date__icontains=search_value)
                | CEC_Module.objects.filter(T_NOCT__icontains=search_value)
                | CEC_Module.objects.filter(A_c__icontains=search_value)
                | CEC_Module.objects.filter(N_s__icontains=search_value)
                | CEC_Module.objects.filter(I_sc_ref__icontains=search_value)
                | CEC_Module.objects.filter(V_oc_ref__icontains=search_value)
                | CEC_Module.objects.filter(I_mp_ref__icontains=search_value)
                | CEC_Module.objects.filter(V_mp_ref__icontains=search_value)
                | CEC_Module.objects.filter(Technology__in=tech_search)
                | CEC_Module.objects.filter(STC__icontains=search_value))
        else:
            cecmod_set = CEC_Module.objects.all()
        col_data = [col["[data]"] for col in columns]
        if len(order):
            order_by_list = [
                ("-" if o['[dir]']=='desc' else "")+col_data[int(o['[column]'])]
                for o in order]
            # XXX: -Name yields "a" first instead of "Z" !
            # handle case-sensitivity descending order for string fields
            if '-Name' in order_by_list:
                name_idx = order_by_list.index('-Name')
                order_by_list[name_idx] = Lower('Name').desc()
            # Technology is an integer field not string
        else:
            order_by_list = []
        cecmod_set = cecmod_set.order_by(*order_by_list)
        filtered_records = cecmod_set.count()
        data = [{
            'id': cecmod.id,
            'Name': cecmod.Name,
            'BIPV': cecmod.BIPV,
            'Date': cecmod.Date,
            'T_NOCT': cecmod.T_NOCT,
            'A_c': cecmod.A_c,
            'N_s': cecmod.N_s,
            'I_sc_ref': cecmod.I_sc_ref,
            'V_oc_ref': cecmod.V_oc_ref,
            'I_mp_ref': cecmod.I_mp_ref,
            'V_mp_ref': cecmod.V_mp_ref,
            'Technology': cecmod.get_Technology_display(),
            'STC': cecmod.STC,}
            for cecmod in cecmod_set[start:limit]]
        response = {
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': filtered_records,
            'data': data}
        return JsonResponse(response)


def cec_modules_tech(request):
    return JsonResponse(dict(CEC_Module.TECH))


def _get_ivcurve(v_oc, params, ivcurve_pnts=100):
    logspace_pts = np.logspace(np.log10(11.0), 0.0, ivcurve_pnts)
    return bishop88(v_oc * (11.0 - logspace_pts) / 10.0, *params)


def cec_module_detail(request, cec_module_id):
    cec_mod = get_object_or_404(CEC_Module, pk=cec_module_id)
    fieldnames = CEC_Module._meta.get_fields()
    cec_mod_dict = {k.name: getattr(cec_mod, k.name) for k in fieldnames}
    # for k in ['IXO', 'IXXO', 'C4', 'C5', 'C6', 'C7']:
    #     if cec_mod_dict[k] is None:
    #         cec_mod_dict[k] = 0.
    celltemps = [0.0, 25.0, 50.0, 75.0, 100.0]
    effirrad = 1000
    results = []
    for tc in celltemps:
        params = calcparams_cec(
            effective_irradiance=effirrad, temp_cell=tc,
            alpha_sc=cec_mod_dict['alpha_sc'],
            a_ref=cec_mod_dict['a_ref'],
            I_L_ref=cec_mod_dict['I_L_ref'],
            I_o_ref=cec_mod_dict['I_o_ref'],
            R_sh_ref=cec_mod_dict['R_sh_ref'],
            R_s=cec_mod_dict['R_s'],
            Adjust=cec_mod_dict['Adjust'])
        result = singlediode(*params, method='newton')
        # ivcurve_pnts deprecated in pvlib-0.10
        ivp = _get_ivcurve(result['v_oc'], params)
        result['i'], result['v'], result['p'] = ivp
        results.append(result)
    current = np.concatenate([r['i'].reshape(1, 100) for r in results], axis=0)
    voltage = np.concatenate([r['v'].reshape(1, 100) for r in results], axis=0)
    # eff = results['p_mp'] / effirrad / cec_mod.Area * 100 / 1000
    fig = figure(
        x_axis_label='voltage, V [V]',
        y_axis_label='current, I [A]',
        title=cec_mod.Name,
        width=800, height=600, sizing_mode='scale_width'
    )
    plot = fig.multi_line(
        voltage.tolist(), current.tolist(), color=cmap, line_width=4)
    legend = Legend(items=[
        LegendItem(label='{:d} [C]'.format(int(ct)), renderers=[plot], index=n)
        for n, ct in enumerate(celltemps)])
    fig.scatter(
        0, [r['i_sc'] for r in results], size=15, color=cmap, marker='square')
    fig.scatter(
        [r['v_oc'] for r in results], 0, size=15, color=cmap)
    fig.scatter(
        [r['v_mp'] for r in results], [r['i_mp'] for r in results], size=15,
        color=cmap, marker='triangle')
    fig.add_layout(legend)
    plot_script, plot_div = components(fig)
    return render(
        request, 'cec_module_detail.html', {
            'path': request.path, 'cec_mod': cec_mod,
            'plot_script': plot_script, 'plot_div': plot_div,
            'cec_mod_dict': cec_mod_dict,
            'cec_mod_tech': dict(CEC_Module.TECH)})


@csrf_exempt
def pvlib(request):
    FORMS = {
        'weatherform': WeatherForm, 'solposform': SolarPositionForm,
        'tl_form': LinkeTurbidityForm, 'am_form': AirmassForm}
    if request.method == 'GET':
        forms = {k: v() for k, v in FORMS.items()}
    elif request.method == 'POST':
        forms = {k: v(request.POST) for k, v in FORMS.items()}
    return render(
        request, 'pvlib.html', {'path': request.path, 'forms': forms})
