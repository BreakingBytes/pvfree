from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator

class SolarPositionForm(forms.Form):
    lat = forms.FloatField(
        label='Latitude',
        validators=[MaxValueValidator(90), MinValueValidator(-90)])
    lon = forms.FloatField(
        label='Lonitude',
        validators=[MaxValueValidator(180), MinValueValidator(-180)])
    start = forms.DateTimeField(label='Start date/time')
    end = forms.DateTimeField(label="End date/time")
    tz = forms.IntegerField(
        label='timezone', required=False,
        validators=[MaxValueValidator(12), MinValueValidator(-12)])
    freq = forms.CharField(label='frequency', max_length=5, required=False)


class LinkeTurbidityForm(forms.Form):
    tl_lat = forms.FloatField(
        label='Latitude',
        validators=[MaxValueValidator(90), MinValueValidator(-90)])
    tl_lon = forms.FloatField(
        label='Lonitude',
        validators=[MaxValueValidator(180), MinValueValidator(-180)])
    tl_start = forms.DateTimeField(label='Start date/time')
    tl_end = forms.DateTimeField(label="End date/time")
    tl_tz = forms.IntegerField(
        label='timezone', required=False,
        validators=[MaxValueValidator(12), MinValueValidator(-12)])
    tl_freq = forms.CharField(label='frequency', max_length=5, required=False)