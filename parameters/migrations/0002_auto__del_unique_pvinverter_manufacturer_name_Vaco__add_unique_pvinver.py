# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'PVInverter', fields ['manufacturer', 'name', 'Vaco']
        db.delete_unique(u'parameters_pvinverter', ['manufacturer', 'name', 'Vaco'])

        # Adding unique constraint on 'PVInverter', fields ['manufacturer', 'name', 'Vaco', 'vintage']
        db.create_unique(u'parameters_pvinverter', ['manufacturer', 'name', 'Vaco', 'vintage'])


    def backwards(self, orm):
        # Removing unique constraint on 'PVInverter', fields ['manufacturer', 'name', 'Vaco', 'vintage']
        db.delete_unique(u'parameters_pvinverter', ['manufacturer', 'name', 'Vaco', 'vintage'])

        # Adding unique constraint on 'PVInverter', fields ['manufacturer', 'name', 'Vaco']
        db.create_unique(u'parameters_pvinverter', ['manufacturer', 'name', 'Vaco'])


    models = {
        u'parameters.pvinverter': {
            'C0': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'C1': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'C2': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'C3': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'Idcmax': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'MPPT_hi': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'MPPT_low': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'Meta': {'unique_together': "(('manufacturer', 'name', 'Vaco', 'vintage'),)", 'object_name': 'PVInverter'},
            'Paco': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'Pdco': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'Pnt': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'Pso': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'Sandia_ID': ('django.db.models.fields.IntegerField', [], {}),
            'Tamb_low': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'Tamb_max': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'Vaco': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'Vdcmax': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'Vdco': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manufacturer': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'numberMPPTChannels': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'vintage': ('django.db.models.fields.DateField', [], {}),
            'weight': ('django.db.models.fields.FloatField', [], {'default': '-999'})
        }
    }

    complete_apps = ['parameters']