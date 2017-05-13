# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PVModule'
        db.create_table(u'parameters_pvmodule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('vintage', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(1999, 1, 1, 0, 0))),
            ('vintage_estimated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('area', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('material', self.gf('django.db.models.fields.IntegerField')(default=10)),
            ('cells_in_series', self.gf('django.db.models.fields.IntegerField')(default=-999)),
            ('parallel_strings', self.gf('django.db.models.fields.IntegerField')(default=-999)),
            ('isc0', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('voc0', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('imp0', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('vmp0', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('ix0', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('ixx0', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('c0', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('c1', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('c2', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('c3', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('c4', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('c5', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('c6', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('c7', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('aisc', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('aimp', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('bvoc0', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('mbvoc', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('bvmp0', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('mbvmp', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('n', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('a0', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('a1', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('a2', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('a3', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('a4', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('b0', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('b1', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('b2', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('b3', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('b4', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('b5', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('dt', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('a', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('b', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'parameters', ['PVModule'])

        # Adding unique constraint on 'PVModule', fields ['name', 'vintage', 'vintage_estimated', 'notes']
        db.create_unique(u'parameters_pvmodule', ['name', 'vintage', 'vintage_estimated', 'notes'])


    def backwards(self, orm):
        # Removing unique constraint on 'PVModule', fields ['name', 'vintage', 'vintage_estimated', 'notes']
        db.delete_unique(u'parameters_pvmodule', ['name', 'vintage', 'vintage_estimated', 'notes'])

        # Deleting model 'PVModule'
        db.delete_table(u'parameters_pvmodule')


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