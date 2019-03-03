import json
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
    FILETYPES = [('CSV', 'CSV'), ('XLSX', 'XLSX'), ('JSON', 'JSON')]
    FILEFIELDS = [
        (0, 'Apparent Zenith'), (1, 'Zenith'), (2, 'Apparent Elevation'),
        (3, 'Elevation'), (4, 'Azimuth')]
    zenith_data = forms.CharField(label='Solar Position Data', required=False, widget=forms.Textarea)
    zenith_file = forms.FileField(label='Solar Position File', required=False)
    filetype = forms.ChoiceField(
        label='File Type', required=False, choices=FILETYPES)
    filecolumns = forms.MultipleChoiceField(
        label='File Fields', choices=FILEFIELDS, required=False)


    def clean_zenith_data(self):
    # https://stackoverflow.com/questions/14626702/django-forms-with-json-fields
        zdata = self.cleaned_data['zenith_data']
        try:
            json.loads(zdata)
        except:
            raise forms.ValidationError("Invalid data in zenith dat")
        return zdata
