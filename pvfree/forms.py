import json
import pandas as pd
from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator


class SolarPositionForm(forms.Form):
    lat = forms.FloatField(
        label='Latitude',
        validators=[MaxValueValidator(90), MinValueValidator(-90)])
    lon = forms.FloatField(
        label='Longitude',
        validators=[MaxValueValidator(180), MinValueValidator(-180)])
    start = forms.DateTimeField(label='Start Timestamp')
    end = forms.DateTimeField(label="End Timestamp")
    tz = forms.IntegerField(
        label='Timezone', required=False,
        validators=[MaxValueValidator(12), MinValueValidator(-12)])
    freq = forms.CharField(label='Frequency', max_length=5, required=False)


class LinkeTurbidityForm(forms.Form):
    tl_lat = forms.FloatField(
        label='Latitude',
        validators=[MaxValueValidator(90), MinValueValidator(-90)])
    tl_lon = forms.FloatField(
        label='Longitude',
        validators=[MaxValueValidator(180), MinValueValidator(-180)])
    tl_start = forms.DateTimeField(label='Start Timestamp')
    tl_end = forms.DateTimeField(label="End Timestamp")
    tl_tz = forms.IntegerField(
        label='Timezone', required=False,
        validators=[MaxValueValidator(12), MinValueValidator(-12)])
    tl_freq = forms.CharField(label='Frequency', max_length=5, required=False)


class AirmassForm(forms.Form):
    FILETYPES = [('csv', 'CSV'), ('xlsx', 'XLSX'), ('json', 'JSON')]
    MODELS = [
        ('simple', 'Simple'), ('kasten1966', 'Kasten, 1966'),
        ('youngirvine1967', 'Young & Irvine, 1967'),
        ('kastenyoung1989', 'Kasten & Young, 1989'),
        ('gueymard1993', 'Gueymard, 1993'), ('young1994', 'Young, 1994'),
        ('pickering2002', 'Pickering, 2002')]
    zenith_data = forms.CharField(
        label='Solar Position Data', required=False, widget=forms.Textarea)
    zenith_file = forms.FileField(label='Solar Position File', required=False)
    filetype = forms.ChoiceField(
        label='File Type', required=False, choices=FILETYPES, initial='json')
    model = forms.ChoiceField(
        label='Model', required=False, initial='kastenyoung1989',
        choices=MODELS)


    def clean_zenith_data(self):
    # https://stackoverflow.com/questions/14626702/django-forms-with-json-fields
        zdata = self.cleaned_data['zenith_data']
        try:
            zenith_data = json.loads(zdata)
            times = pd.DatetimeIndex(zenith_data.keys())  # keys not necessary
            columns = {}
            for row in zenith_data.values():
                if not columns:
                    columns = {k: [float(v)] for k, v in row.items()}
                else:
                    for k, v in row.items():
                        columns[k].append(float(v))
        except:
            raise forms.ValidationError("Invalid data in zenith data")
        return zdata


class WeatherForm(forms.Form):
    SRCS = [
        ('pvgis', 'PVGIS'), ('psm3', 'PSM3'), ('tmy2', 'TMY2'),
        ('tmy3', 'TMY3')]
    tmy_lat = forms.FloatField(
        label='Latitude',
        validators=[MaxValueValidator(90), MinValueValidator(-90)])
    tmy_lon = forms.FloatField(
        label='Longitude',
        validators=[MaxValueValidator(180), MinValueValidator(-180)])
    tmy_start_year = forms.DateField(label='Start Date', required=False)
    tmy_end_year = forms.DateField(label="End Date", required=False)
    tmy = forms.BooleanField(label='TMY', required=False)
    tmy_source = forms.ChoiceField(
        label='Source', required=False, initial='PVGIS',
        choices=SRCS)
    tmy_file = forms.FileField(required=False, label="TMY file")
