# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parameters', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CEC_Module',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Name', models.CharField(unique=True, max_length=100)),
                ('BIPV', models.BooleanField()),
                ('Date', models.DateField()),
                ('T_NOCT', models.FloatField()),
                ('A_c', models.FloatField()),
                ('N_s', models.FloatField()),
                ('I_sc_ref', models.FloatField()),
                ('V_oc_ref', models.FloatField()),
                ('I_mp_ref', models.FloatField()),
                ('V_mp_ref', models.FloatField()),
                ('alpha_sc', models.FloatField()),
                ('beta_oc', models.FloatField()),
                ('a_ref', models.FloatField()),
                ('I_L_ref', models.FloatField()),
                ('I_o_ref', models.FloatField()),
                ('R_s', models.FloatField()),
                ('R_sh_ref', models.FloatField()),
                ('Adjust', models.FloatField()),
                ('gamma_r', models.FloatField()),
                ('Version', models.IntegerField(default=0, blank=True, choices=[(0, b''), (1, b'MM105'), (2, b'MM106'), (3, b'MM107'), (4, b'NRELv1')])),
                ('PTC', models.FloatField()),
                ('Technology', models.IntegerField(choices=[(0, b'1-a-Si'), (1, b'2-a-Si'), (2, b'3-a-Si'), (3, b'CIGS'), (4, b'CIS'), (5, b'CdTe'), (6, b'HIT-Si'), (7, b'Mono-c-Si'), (8, b'Multi-c-Si'), (9, b'Thin Film'), (10, b'a-Si'), (11, b'a-Si/nc')])),
            ],
        ),
    ]
