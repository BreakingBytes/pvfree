# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'PVModule.C7'
        db.alter_column(u'parameters_pvmodule', 'C7', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'PVModule.C6'
        db.alter_column(u'parameters_pvmodule', 'C6', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'PVModule.C5'
        db.alter_column(u'parameters_pvmodule', 'C5', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'PVModule.C4'
        db.alter_column(u'parameters_pvmodule', 'C4', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'PVModule.IXO'
        db.alter_column(u'parameters_pvmodule', 'IXO', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'PVModule.IXXO'
        db.alter_column(u'parameters_pvmodule', 'IXXO', self.gf('django.db.models.fields.FloatField')(null=True))

    def backwards(self, orm):

        # Changing field 'PVModule.C7'
        db.alter_column(u'parameters_pvmodule', 'C7', self.gf('django.db.models.fields.FloatField')(default=nan))

        # Changing field 'PVModule.C6'
        db.alter_column(u'parameters_pvmodule', 'C6', self.gf('django.db.models.fields.FloatField')(default=nan))

        # Changing field 'PVModule.C5'
        db.alter_column(u'parameters_pvmodule', 'C5', self.gf('django.db.models.fields.FloatField')(default=nan))

        # Changing field 'PVModule.C4'
        db.alter_column(u'parameters_pvmodule', 'C4', self.gf('django.db.models.fields.FloatField')(default=nan))

        # Changing field 'PVModule.IXO'
        db.alter_column(u'parameters_pvmodule', 'IXO', self.gf('django.db.models.fields.FloatField')(default=nan))

        # Changing field 'PVModule.IXXO'
        db.alter_column(u'parameters_pvmodule', 'IXXO', self.gf('django.db.models.fields.FloatField')(default=nan))

    models = {
        u'parameters.pvinverter': {
            'C0': ('django.db.models.fields.FloatField', [], {}),
            'C1': ('django.db.models.fields.FloatField', [], {}),
            'C2': ('django.db.models.fields.FloatField', [], {}),
            'C3': ('django.db.models.fields.FloatField', [], {}),
            'Idcmax': ('django.db.models.fields.FloatField', [], {}),
            'Meta': {'object_name': 'PVInverter'},
            'Mppt_high': ('django.db.models.fields.FloatField', [], {}),
            'Mppt_low': ('django.db.models.fields.FloatField', [], {}),
            'Name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'Paco': ('django.db.models.fields.FloatField', [], {}),
            'Pdco': ('django.db.models.fields.FloatField', [], {}),
            'Pnt': ('django.db.models.fields.FloatField', [], {}),
            'Pso': ('django.db.models.fields.FloatField', [], {}),
            'Vac': ('django.db.models.fields.FloatField', [], {}),
            'Vdcmax': ('django.db.models.fields.FloatField', [], {}),
            'Vdco': ('django.db.models.fields.FloatField', [], {}),
            'created_on': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_on': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'parameters.pvmodule': {
            'A': ('django.db.models.fields.FloatField', [], {}),
            'A0': ('django.db.models.fields.FloatField', [], {}),
            'A1': ('django.db.models.fields.FloatField', [], {}),
            'A2': ('django.db.models.fields.FloatField', [], {}),
            'A3': ('django.db.models.fields.FloatField', [], {}),
            'A4': ('django.db.models.fields.FloatField', [], {}),
            'Aimp': ('django.db.models.fields.FloatField', [], {}),
            'Aisc': ('django.db.models.fields.FloatField', [], {}),
            'Area': ('django.db.models.fields.FloatField', [], {}),
            'B': ('django.db.models.fields.FloatField', [], {}),
            'B0': ('django.db.models.fields.FloatField', [], {}),
            'B1': ('django.db.models.fields.FloatField', [], {}),
            'B2': ('django.db.models.fields.FloatField', [], {}),
            'B3': ('django.db.models.fields.FloatField', [], {}),
            'B4': ('django.db.models.fields.FloatField', [], {}),
            'B5': ('django.db.models.fields.FloatField', [], {}),
            'Bvmpo': ('django.db.models.fields.FloatField', [], {}),
            'Bvoco': ('django.db.models.fields.FloatField', [], {}),
            'C0': ('django.db.models.fields.FloatField', [], {}),
            'C1': ('django.db.models.fields.FloatField', [], {}),
            'C2': ('django.db.models.fields.FloatField', [], {}),
            'C3': ('django.db.models.fields.FloatField', [], {}),
            'C4': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'C5': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'C6': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'C7': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Cells_in_Series': ('django.db.models.fields.IntegerField', [], {}),
            'DTC': ('django.db.models.fields.FloatField', [], {}),
            'FD': ('django.db.models.fields.FloatField', [], {}),
            'IXO': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'IXXO': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Impo': ('django.db.models.fields.FloatField', [], {}),
            'Isco': ('django.db.models.fields.FloatField', [], {}),
            'Material': ('django.db.models.fields.IntegerField', [], {}),
            'Mbvmp': ('django.db.models.fields.FloatField', [], {}),
            'Mbvoc': ('django.db.models.fields.FloatField', [], {}),
            'Meta': {'unique_together': "(('Name', 'Vintage', 'Notes'),)", 'object_name': 'PVModule'},
            'N': ('django.db.models.fields.FloatField', [], {}),
            'Name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'Notes': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'Parallel_Strings': ('django.db.models.fields.IntegerField', [], {}),
            'Vintage': ('django.db.models.fields.DateField', [], {}),
            'Vmpo': ('django.db.models.fields.FloatField', [], {}),
            'Voco': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_vintage_estimated': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['parameters']