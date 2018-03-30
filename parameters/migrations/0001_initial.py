# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PVInverter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Name', models.CharField(unique=True, max_length=100)),
                ('Vac', models.FloatField(verbose_name=b'AC Voltage [V]')),
                ('Paco', models.FloatField(verbose_name=b'Rated AC power [W]')),
                ('Pdco', models.FloatField(verbose_name=b'DC power [W]')),
                ('Vdco', models.FloatField(verbose_name=b'DC voltage [V]')),
                ('Pso', models.FloatField(verbose_name=b'Self consumption [W]')),
                ('C0', models.FloatField()),
                ('C1', models.FloatField()),
                ('C2', models.FloatField()),
                ('C3', models.FloatField()),
                ('Pnt', models.FloatField(verbose_name=b'Nighttime consumption [W]')),
                ('Vdcmax', models.FloatField(verbose_name=b'Max DC voltage [V]')),
                ('Idcmax', models.FloatField(verbose_name=b'Max DC current [A]')),
                ('Mppt_low', models.FloatField(verbose_name=b'Lower bound of MPPT [W]')),
                ('Mppt_high', models.FloatField(verbose_name=b'Higher bound of MPPT [W]')),
                ('created_on', models.DateField(auto_now_add=True)),
                ('modified_on', models.DateField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Inverter',
            },
        ),
        migrations.CreateModel(
            name='PVModule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Name', models.CharField(max_length=100)),
                ('Vintage', models.DateField()),
                ('Area', models.FloatField()),
                ('Material', models.IntegerField(choices=[(1, b'2-a-Si'), (2, b'3-a-Si'), (3, b'CIS'), (4, b'CdTe'), (5, b'EFG mc-Si'), (6, b'GaAs'), (7, b'HIT-Si'), (8, b'Si-Film'), (9, b'a-Si / mono-Si'), (10, b'c-Si'), (11, b'mc-Si')])),
                ('Cells_in_Series', models.IntegerField()),
                ('Parallel_Strings', models.IntegerField()),
                ('Isco', models.FloatField(verbose_name=b'Short Circuit Current [A]')),
                ('Voco', models.FloatField(verbose_name=b'Open Circuit Voltage [V]')),
                ('Impo', models.FloatField(verbose_name=b'Max Power Current [A]')),
                ('Vmpo', models.FloatField(verbose_name=b'Max Power Voltage [V]')),
                ('Aisc', models.FloatField(verbose_name=b'Short Circuit Current Tempco')),
                ('Aimp', models.FloatField(verbose_name=b'Max Power Current Tempco')),
                ('C0', models.FloatField()),
                ('C1', models.FloatField()),
                ('Bvoco', models.FloatField(verbose_name=b'Open Circuit Voltage Tempco')),
                ('Mbvoc', models.FloatField()),
                ('Bvmpo', models.FloatField(verbose_name=b'Max Power Voltage Tempco')),
                ('Mbvmp', models.FloatField()),
                ('N', models.FloatField(verbose_name=b'Diode Ideality Factor')),
                ('C2', models.FloatField()),
                ('C3', models.FloatField()),
                ('A0', models.FloatField()),
                ('A1', models.FloatField()),
                ('A2', models.FloatField()),
                ('A3', models.FloatField()),
                ('A4', models.FloatField()),
                ('B0', models.FloatField()),
                ('B1', models.FloatField()),
                ('B2', models.FloatField()),
                ('B3', models.FloatField()),
                ('B4', models.FloatField()),
                ('B5', models.FloatField()),
                ('DTC', models.FloatField(verbose_name=b'Cell Temp Delta')),
                ('FD', models.FloatField(verbose_name=b'Diffuse Fraction')),
                ('A', models.FloatField(verbose_name=b'Natural Convection Coeff')),
                ('B', models.FloatField(verbose_name=b'Forced Convection Coeff')),
                ('C4', models.FloatField(null=True, blank=True)),
                ('C5', models.FloatField(null=True, blank=True)),
                ('IXO', models.FloatField(null=True, blank=True)),
                ('IXXO', models.FloatField(null=True, blank=True)),
                ('C6', models.FloatField(null=True, blank=True)),
                ('C7', models.FloatField(null=True, blank=True)),
                ('Notes', models.CharField(max_length=100)),
                ('is_vintage_estimated', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Module',
            },
        ),
        migrations.AlterUniqueTogether(
            name='pvmodule',
            unique_together=set([('Name', 'Vintage', 'Notes')]),
        ),
    ]
