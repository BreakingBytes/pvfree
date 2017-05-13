# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'PVModule.fd'
        db.add_column(u'parameters_pvmodule', 'fd',
                      self.gf('django.db.models.fields.FloatField')(default=-999),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'PVModule.fd'
        db.delete_column(u'parameters_pvmodule', 'fd')


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
            'vintage': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(1999, 1, 1, 0, 0)'}),
            'weight': ('django.db.models.fields.FloatField', [], {'default': '-999'})
        },
        u'parameters.pvmodule': {
            'Meta': {'unique_together': "(('name', 'vintage', 'vintage_estimated', 'notes'),)", 'object_name': 'PVModule'},
            'a': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'a0': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'a1': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'a2': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'a3': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'a4': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'aimp': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'aisc': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'area': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'b': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'b0': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'b1': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'b2': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'b3': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'b4': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'b5': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'bvmp0': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'bvoc0': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'c0': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'c1': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'c2': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'c3': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'c4': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'c5': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'c6': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'c7': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'cells_in_series': ('django.db.models.fields.IntegerField', [], {'default': '-999'}),
            'dt': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'fd': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imp0': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'isc0': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'ix0': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'ixx0': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'material': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'mbvmp': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'mbvoc': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'n': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parallel_strings': ('django.db.models.fields.IntegerField', [], {'default': '-999'}),
            'vintage': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(1999, 1, 1, 0, 0)'}),
            'vintage_estimated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'vmp0': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'voc0': ('django.db.models.fields.FloatField', [], {'default': '-999'})
        }
    }

    complete_apps = ['parameters']