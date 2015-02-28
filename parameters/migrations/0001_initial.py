# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PVInverter'
        db.create_table(u'parameters_pvinverter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Sandia_ID', self.gf('django.db.models.fields.IntegerField')()),
            ('manufacturer', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('vintage', self.gf('django.db.models.fields.DateField')()),
            ('Paco', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('Vaco', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('Pdco', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('Vdco', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('Pso', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('C0', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('C1', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('C2', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('C3', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('Vdcmax', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('Idcmax', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('MPPT_low', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('MPPT_hi', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('Pnt', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('Tamb_low', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('Tamb_max', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('weight', self.gf('django.db.models.fields.FloatField')(default=-999)),
            ('numberMPPTChannels', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal(u'parameters', ['PVInverter'])

        # Adding unique constraint on 'PVInverter', fields ['manufacturer', 'name', 'Vaco']
        db.create_unique(u'parameters_pvinverter', ['manufacturer', 'name', 'Vaco'])


    def backwards(self, orm):
        # Removing unique constraint on 'PVInverter', fields ['manufacturer', 'name', 'Vaco']
        db.delete_unique(u'parameters_pvinverter', ['manufacturer', 'name', 'Vaco'])

        # Deleting model 'PVInverter'
        db.delete_table(u'parameters_pvinverter')


    models = {
        u'parameters.pvinverter': {
            'C0': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'C1': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'C2': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'C3': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'Idcmax': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'MPPT_hi': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'MPPT_low': ('django.db.models.fields.FloatField', [], {'default': '-999'}),
            'Meta': {'unique_together': "(('manufacturer', 'name', 'Vaco'),)", 'object_name': 'PVInverter'},
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