from django.shortcuts import render, redirect
from parameters.models import PVInverter, PVModule, CEC_Module
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import FieldError


@login_required(redirect_field_name=None, login_url='/admin/')
def file_upload(request):
    user = request.user
    if request.method == 'POST':
        upload_file = request.FILES.get('uploadFile')
        upload_select = request.POST.get('uploadSelect')
        sam_version_select = request.POST.get('samVersionSelect')
        if upload_file is not None:
            try:
                if upload_select == 'Sandia Modules':
                    PVModule.upload(upload_file, user)
                elif upload_select == 'CEC Inverters':
                    PVInverter.upload(upload_file, user, sam_version_select)
                elif upload_select == 'CEC Modules':
                    CEC_Module.upload(upload_file, user)
                else:
                    raise KeyError('Selection "{}" is not valid.'.format(
                        upload_select))
            except (KeyError, FieldError) as exc:
                messages.error(request,
                    'File "{}" has wrong format for {}. -- {}'.format(
                        upload_file.name, upload_select, exc))
            else:
                messages.success(request,
                    'Uploaded {} file "{}" successfully.'.format(
                        upload_select, upload_file.name))
        else:
            messages.warning(request, 'No file selected.')
        return redirect(request.POST.get('next', 'home'))
    return redirect('home')
