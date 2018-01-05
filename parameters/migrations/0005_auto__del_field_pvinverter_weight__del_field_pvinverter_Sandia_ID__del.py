# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'PVInverter', fields ['manufacturer', 'name', 'Vaco', 'vintage']
        db.delete_unique(u'parameters_pvinverter', ['manufacturer', 'name', 'Vaco', 'vintage'])

        # Deleting field 'PVInverter.weight'
        db.delete_column(u'parameters_pvinverter', 'weight')

        # Deleting field 'PVInverter.Sandia_ID'
        db.delete_column(u'parameters_pvinverter', 'Sandia_ID')

        # Deleting field 'PVInverter.vintage'
        db.delete_column(u'parameters_pvinverter', 'vintage')

        # Deleting field 'PVInverter.source'
        db.delete_column(u'parameters_pvinverter', 'source')

        # Rename field 'PVInverter.MPPT_low'
        db.rename_column(u'parameters_pvinverter', 'MPPT_low', 'Mppt_low')

        # Alter field 'PVInverter.Mppt_low'
        db.alter_column(u'parameters_pvinverter', 'Mppt_low',
                      self.gf('django.db.models.fields.FloatField')(default=-999))

        # Deleting field 'PVInverter.Tamb_low'
        db.delete_column(u'parameters_pvinverter', 'Tamb_low')

        # Rename field 'PVInverter.MPPT_hi'
        db.rename_column(u'parameters_pvinverter', 'MPPT_hi', 'Mppt_high')

        # Alter field 'PVInverter.Mppt_high'
        db.alter_column(u'parameters_pvinverter', 'Mppt_high',
                      self.gf('django.db.models.fields.FloatField')(default=-999))

        # Deleting field 'PVInverter.manufacturer'
        db.delete_column(u'parameters_pvinverter', 'manufacturer')

        # Rename field 'PVInverter.name'
        db.rename_column(u'parameters_pvinverter', 'name', 'Name')

        # Alter field 'PVInverter.Name'
        db.alter_column(u'parameters_pvinverter', 'Name',
                      self.gf('django.db.models.fields.CharField')(default='my-inverter-name', max_length=100, primary_key=True))

        # Deleting field 'PVInverter.Tamb_max'
        db.delete_column(u'parameters_pvinverter', 'Tamb_max')

        # Rename field 'PVInverter.Vaco'
        db.rename_column(u'parameters_pvinverter', 'Vaco', 'Vac')

        # Alter field 'PVInverter.Vac'
        db.alter_column(u'parameters_pvinverter', 'Vac',
                      self.gf('django.db.models.fields.FloatField')(default=-999))

        # Deleting field 'PVInverter.numberMPPTChannels'
        db.delete_column(u'parameters_pvinverter', 'numberMPPTChannels')

        # Adding field 'PVInverter.created_on'
        db.add_column(u'parameters_pvinverter', 'created_on',
                      self.gf('django.db.models.fields.DateField')(auto_now_add=True, default=datetime.datetime(1999, 1, 1, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'PVInverter.modified_on'
        db.add_column(u'parameters_pvinverter', 'modified_on',
                      self.gf('django.db.models.fields.DateField')(auto_now=True, default=datetime.datetime(1999, 1, 1, 0, 0), blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'PVInverter.weight'
        db.add_column(u'parameters_pvinverter', 'weight',
                      self.gf('django.db.models.fields.FloatField')(default=-999),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PVInverter.Sandia_ID'
        raise RuntimeError("Cannot reverse this migration. 'PVInverter.Sandia_ID' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PVInverter.Sandia_ID'
        db.add_column(u'parameters_pvinverter', 'Sandia_ID',
                      self.gf('django.db.models.fields.IntegerField')(),
                      keep_default=False)


        # Adding field 'PVInverter.vintage'
        db.add_column(u'parameters_pvinverter', 'vintage',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(1999, 1, 1, 0, 0)),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PVInverter.source'
        raise RuntimeError("Cannot reverse this migration. 'PVInverter.source' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PVInverter.source'
        db.add_column(u'parameters_pvinverter', 'source',
                      self.gf('django.db.models.fields.CharField')(max_length=10),
                      keep_default=False)


        # Deleting field 'PVInverter.Mppt_low'
        db.rename_column(u'parameters_pvinverter', 'Mppt_low', 'MPPT_low')

        # Adding field 'PVInverter.MPPT_low'
        db.alter_column(u'parameters_pvinverter', 'MPPT_low',
                      self.gf('django.db.models.fields.FloatField')(default=-999))

        # Adding field 'PVInverter.Tamb_low'
        db.add_column(u'parameters_pvinverter', 'Tamb_low',
                      self.gf('django.db.models.fields.FloatField')(default=-999),
                      keep_default=False)

        # Deleting field 'PVInverter.Mppt_high'
        db.rename_column(u'parameters_pvinverter', 'Mppt_high',  'MPPT_hi')

        # Adding field 'PVInverter.MPPT_hi'
        db.alter_column(u'parameters_pvinverter', 'MPPT_hi',
                      self.gf('django.db.models.fields.FloatField')(default=-999))


        # User chose to not deal with backwards NULL issues for 'PVInverter.manufacturer'
        raise RuntimeError("Cannot reverse this migration. 'PVInverter.manufacturer' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PVInverter.manufacturer'
        db.add_column(u'parameters_pvinverter', 'manufacturer',
                      self.gf('django.db.models.fields.CharField')(max_length=100),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PVInverter.name'
        raise RuntimeError("Cannot reverse this migration. 'PVInverter.name' and its values cannot be restored.")

        # Deleting field 'PVInverter.Name'
        db.rename_column(u'parameters_pvinverter', 'Name', 'name')
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PVInverter.name'
        db.alter_column(u'parameters_pvinverter', 'name',
                      self.gf('django.db.models.fields.CharField')(max_length=100))

        # Adding field 'PVInverter.Tamb_max'
        db.add_column(u'parameters_pvinverter', 'Tamb_max',
                      self.gf('django.db.models.fields.FloatField')(default=-999),
                      keep_default=False)

        # Deleting field 'PVInverter.Vac'
        db.rename_column(u'parameters_pvinverter', 'Vac', 'Vaco')

        # Adding field 'PVInverter.Vaco'
        db.alter_column(u'parameters_pvinverter', 'Vaco',
                      self.gf('django.db.models.fields.FloatField')(default=-999))

        # Adding field 'PVInverter.numberMPPTChannels'
        db.add_column(u'parameters_pvinverter', 'numberMPPTChannels',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Deleting field 'PVInverter.created_on'
        db.delete_column(u'parameters_pvinverter', 'created_on')

        # Deleting field 'PVInverter.modified_on'
        db.delete_column(u'parameters_pvinverter', 'modified_on')

        # Adding unique constraint on 'PVInverter', fields ['manufacturer', 'name', 'Vaco', 'vintage']
        db.create_unique(u'parameters_pvinverter', ['manufacturer', 'name', 'Vaco', 'vintage'])


    models = {
        u'parameters.pvinverter': {
            'C0': ('django.db.models.fields.FloatField', [], {}),
            'C1': ('django.db.models.fields.FloatField', [], {}),
            'C2': ('django.db.models.fields.FloatField', [], {}),
            'C3': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'Idcmax': ('django.db.models.fields.FloatField', [], {}),
            'Meta': {'object_name': 'PVInverter'},
            'Mppt_high': ('django.db.models.fields.FloatField', [], {}),
            'Mppt_low': ('django.db.models.fields.FloatField', [], {}),
            'Name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
            'Paco': ('django.db.models.fields.FloatField', [], {}),
            'Pdco': ('django.db.models.fields.FloatField', [], {}),
            'Pnt': ('django.db.models.fields.FloatField', [], {}),
            'Pso': ('django.db.models.fields.FloatField', [], {}),
            'Vac': ('django.db.models.fields.FloatField', [], {}),
            'Vdcmax': ('django.db.models.fields.FloatField', [], {}),
            'Vdco': ('django.db.models.fields.FloatField', [], {}),
            'created_on': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'modified_on': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'})
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