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
    # PVGIS 5.1:
    #   NSRDB: 2005 - 2015 (North America)
    #   SARAH: 2005 - 2016 (South America, Europe, Africa)
    #   ERA5: 2005 - 2016 (Europe)
    #   COSMO: 2005 - 2016 (Europe)
    #   CMSAF: 2007 - 2016 (Europe, Africa)
    YEAR_NAMES = [
        1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009,
        2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
    YEAR_NAMES = list(zip(YEAR_NAMES, YEAR_NAMES))
    SRCS = [
        ('pvgis', 'PVGIS'), ('psm3', 'PSM3'), ('tmy2', 'TMY2'),
        ('tmy3', 'TMY3')]
    FREQ = [5, 15, 30, 60]
    FREQ = list(zip(FREQ, FREQ))
    #[(5, '5'), (15, '15'), (30, '30'), (60, '60')]
    tmy_lat = forms.FloatField(
        label='Latitude',
        validators=[MaxValueValidator(90), MinValueValidator(-90)])
    tmy_lon = forms.FloatField(
        label='Longitude',
        validators=[MaxValueValidator(180), MinValueValidator(-180)])
    tmy_year_name = forms.ChoiceField(
        label='Year Name', required=False, initial=2020, choices=YEAR_NAMES)
    tmy_coerced_year = forms.IntegerField(
        label="Coerced Year", required=False, initial=1990,
        validators=[MaxValueValidator(2050), MinValueValidator(1950)])
    tmy_freq = forms.ChoiceField(
        label='Frequency', required=False, initial=60, choices=FREQ)
    tmy_source = forms.ChoiceField(
        label='Source', required=False, initial='psm3',
        choices=SRCS)
    tmy = forms.BooleanField(label='TMY', required=False, initial=True)
    tmy_nrel_key = forms.CharField(
        max_length=100, label='NREL API Key', initial="DEMO_KEY",
        required=False)
    tmy_email = forms.EmailField(
        max_length=100, label='Email Address', required=False)
    tmy_file = forms.FileField(required=False, label="TMY file")
