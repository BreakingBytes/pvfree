from django.shortcuts import render, redirect
from parameters.models import PVInverter, PVModule, CEC_Module
from django.contrib.auth.decorators import login_required


@login_required(redirect_field_name=None, login_url='/admin/')
def file_upload(request):
    if request.method == 'POST':
        upload_file = request.FILES['uploadFile']
        upload_select = request.POST['uploadSelect']
        if upload_select == 'Sandia Modules':
            PVModule.upload(upload_file)
        elif upload_select == 'CEC Inverters':
            PVInverter.upload(upload_file)
        elif upload_select == 'CEC Modules':
            CEC_Module.upload(upload_file)
        else:
            pass
        return redirect(request.POST['next'])
    return render(request, 'index.html')
