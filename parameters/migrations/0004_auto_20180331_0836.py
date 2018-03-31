# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parameters', '0003_auto_20180331_0602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cec_module',
            name='N_s',
            field=models.IntegerField(),
        ),
    ]
