# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parameters', '0002_cec_module'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cec_module',
            options={'verbose_name': 'CEC Module'},
        ),
    ]
