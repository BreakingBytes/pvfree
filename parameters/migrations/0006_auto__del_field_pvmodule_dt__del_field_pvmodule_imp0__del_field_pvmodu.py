# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'PVModule', fields ['name', 'vintage', 'vintage_estimated', 'notes']
        db.delete_unique(u'parameters_pvmodule', ['name', 'vintage', 'vintage_estimated', 'notes'])

        # Deleting field 'PVModule.dt'
        db.rename_column(u'parameters_pvmodule', 'dt', 'DTC')

        # Adding field 'PVModule.DTC'
        db.alter_column(u'parameters_pvmodule', 'DTC',
                      self.gf('django.db.models.fields.FloatField')(default=0))

        # Deleting field 'PVModule.imp0'
        db.rename_column(u'parameters_pvmodule', 'imp0', 'Impo')

        # Adding field 'PVModule.Impo'
        db.alter_column(u'parameters_pvmodule', 'Impo',
                      self.gf('django.db.models.fields.FloatField')(default=0))

        # Deleting field 'PVModule.area'
        db.rename_column(u'parameters_pvmodule', 'area', 'Area')

        # Adding field 'PVModule.Area'
        db.alter_column(u'parameters_pvmodule', 'Area',
                      self.gf('django.db.models.fields.FloatField')(default=-999))

        # Deleting field 'PVModule.bvmp0'
        db.rename_column(u'parameters_pvmodule', 'bvmp0', 'Bvmpo')

        # Adding field 'PVModule.Bvmpo'
        db.alter_column(u'parameters_pvmodule', 'Bvmpo',
                      self.gf('django.db.models.fields.FloatField')(default=0))

        # Deleting field 'PVModule.a'
        db.rename_column(u'parameters_pvmodule', 'a', 'A')

        # Adding field 'PVModule.A'
        db.alter_column(u'parameters_pvmodule', 'A',
                      self.gf('django.db.models.fields.FloatField')(default=0))

        # Deleting field 'PVModule.mbvmp'
        db.rename_column(u'parameters_pvmodule', 'mbvmp', 'Mbvmp')

        # Adding field 'PVModule.Mbvmp'
        db.alter_column(u'parameters_pvmodule', 'Mbvmp',
                      self.gf('django.db.models.fields.FloatField')(default=0))

        # Deleting field 'PVModule.material'
        db.rename_column(u'parameters_pvmodule', 'material', 'Material')

        # Adding field 'PVModule.Material'
        db.alter_column(u'parameters_pvmodule', 'Material',
                      self.gf('django.db.models.fields.IntegerField')(default=10))

        # Deleting field 'PVModule.c3'
        db.rename_column(u'parameters_pvmodule', 'c3', 'C3')

        # Deleting field 'PVModule.c2'
        db.rename_column(u'parameters_pvmodule', 'c2', 'C2')

        # Adding field 'PVModule.C2'
        db.alter_column(u'parameters_pvmodule', 'C2',
                      self.gf('django.db.models.fields.FloatField')(default=0))

        # Adding field 'PVModule.C3'
        db.alter_column(u'parameters_pvmodule', 'C3',
                      self.gf('django.db.models.fields.FloatField')(default=0))

        # Deleting field 'PVModule.c1'
        db.rename_column(u'parameters_pvmodule', 'c1', 'C1')

        # Adding field 'PVModule.C1'
        db.alter_column(u'parameters_pvmodule', 'C1',
                      self.gf('django.db.models.fields.FloatField')(default=0))

        # Deleting field 'PVModule.c0'
        db.rename_column(u'parameters_pvmodule', 'c0', 'C0')

        # Adding field 'PVModule.C0'
        db.alter_column(u'parameters_pvmodule', 'C0',
                      self.gf('django.db.models.fields.FloatField')(default=0))

        # Deleting field 'PVModule.c7'
        db.rename_column(u'parameters_pvmodule', 'c7', 'C7')

        # Deleting field 'PVModule.c6'
        db.rename_column(u'parameters_pvmodule', 'c6', 'C6')

        # Deleting field 'PVModule.c5'
        db.rename_column(u'parameters_pvmodule', 'c5', 'C5')

        # Deleting field 'PVModule.c4'
        db.rename_column(u'parameters_pvmodule', 'c4', 'C4')

        # Deleting field 'PVModule.b'
        db.rename_column(u'parameters_pvmodule', 'b', 'B')

        # Adding field 'PVModule.B'
        db.alter_column(u'parameters_pvmodule', 'B',
                      self.gf('django.db.models.fields.FloatField')(default=0))

        # Deleting field 'PVModule.name'
        db.rename_column(u'parameters_pvmodule', 'name', 'Name')

        # Adding field 'PVModule.Name'
        db.alter_column(u'parameters_pvmodule', 'Name',
                      self.gf('django.db.models.fields.CharField')(default='my-module-name', max_length=100))

        # Deleting field 'PVModule.notes'
        db.rename_column(u'parameters_pvmodule', 'notes', 'Notes')

        # Adding field 'PVModule.Notes'
        db.alter_column(u'parameters_pvmodule', 'Notes',
                      self.gf('django.db.models.fields.CharField')(default='my notes', max_length=100))

        # Deleting field 'PVModule.aimp'
        db.rename_column(u'parameters_pvmodule', 'aimp', 'Aimp')

        # Adding field 'PVModule.Aimp'
        db.alter_column(u'parameters_pvmodule', 'Aimp',
                      self.gf('django.db.models.fields.FloatField')(default=0))

        # Deleting field 'PVModule.n'
        db.rename_column(u'parameters_pvmodule', 'n', 'N')

        # Adding field 'PVModule.N'
        db.alter_column(u'parameters_pvmodule', 'N',
                      self.gf('django.db.models.fields.FloatField')(default=0))

        # Deleting field 'PVModule.ix0'
        db.rename_column(u'parameters_pvmodule', 'ix0', 'IXO')

        # Adding field 'PVModule.IXO'
        db.alter_column(u'parameters_pvmodule', 'IXO',
                      self.gf('django.db.models.fields.FloatField')(default=0))

        # Deleting field 'PVModule.isc0'
        db.rename_column(u'parameters_pvmodule', 'isc0', 'Isco')

        # Adding field 'PVModule.Isco'
        db.alter_column(u'parameters_pvmodule', 'Isco',
                      self.gf('django.db.models.fields.FloatField')(default=0))

        # Deleting field 'PVModule.b4'
        db.rename_column(u'parameters_pvmodule', 'b4', 'B4')

        # Deleting field 'PVModule.b5'
        db.rename_column(u'parameters_pvmodule', 'b5', 'B5')

        # Deleting field 'PVModule.b0'
        db.rename_column(u'parameters_pvmodule', 'b0', 'B0')

        # Deleting field 'PVModule.b1'
        db.rename_column(u'parameters_pvmodule', 'b1', 'B1')

        # Deleting field 'PVModule.b2'
        db.rename_column(u'parameters_pvmodule', 'b2', 'B2')

        # Deleting field 'PVModule.b3'
        db.rename_column(u'parameters_pvmodule', 'b3', 'B3')

        # Adding field 'PVModule.B0'
        db.alter_column(u'parameters_pvmodule', 'B0',
                      self.gf('django.db.models.fields.FloatField')(default=0))

        # Adding field 'PVModule.B1'
        db.alter_column(u'parameters_pvmodule', 'B1',
                      self.gf('django.db.models.fields.FloatField')(default=0))

        # Adding field 'PVModule.B2'
        db.alter_column(u'parameters_pvmodule', 'B2',
                      self.gf('django.db.models.fields.FloatField')(default=0))

        # Adding field 'PVModule.B3'
        db.alter_column(u'parameters_pvmodule', 'B3',
                      self.gf('django.db.models.fields.FloatField')(default=0))

        # Adding field 'PVModule.B4'
        db.alter_column(u'parameters_pvmodule', 'B4',
                      self.gf('django.db.models.fields.FloatField')(default=0))

        # Adding field 'PVModule.B5'
        db.alter_column(u'parameters_pvmodule', 'B5',
                      self.gf('django.db.models.fields.FloatField')(default=0))

        # Deleting field 'PVModule.vmp0'
        db.rename_column(u'parameters_pvmodule', 'vmp0', 'Vmpo')

        # Adding field 'PVModule.Vmpo'
        db.alter_column(u'parameters_pvmodule', 'Vmpo',
                      self.gf('django.db.models.fields.FloatField')(default=0))

        # Deleting field 'PVModule.vintage'
        db.rename_column(u'parameters_pvmodule', 'vintage', 'Vintage')

        # Adding field 'PVModule.Vintage'
        db.alter_column(u'parameters_pvmodule', 'Vintage',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2018, 1, 7, 0, 0)))

        # Deleting field 'PVModule.voc0'
        db.rename_column(u'parameters_pvmodule', 'voc0', 'Voco')

        # Adding field 'PVModule.Voco'
        db.alter_column(u'parameters_pvmodule', 'Voco',
                      self.gf('django.db.models.fields.FloatField')(default=0))

        # Deleting field 'PVModule.parallel_strings'
        db.rename_column(u'parameters_pvmodule', 'parallel_strings', 'Parallel_Strings')

        # Adding field 'PVModule.Parallel_Strings'
        db.alter_column(u'parameters_pvmodule', 'Parallel_Strings',
                      self.gf('django.db.models.fields.IntegerField')(default=1))

        # Deleting field 'PVModule.cells_in_series'
        db.rename_column(u'parameters_pvmodule', 'cells_in_series', 'Cells_in_Series')

        # Adding field 'PVModule.Cells_in_Series'
        db.alter_column(u'parameters_pvmodule', 'Cells_in_Series',
                      self.gf('django.db.models.fields.IntegerField')(default=72))

        # Deleting field 'PVModule.mbvoc'
        db.rename_column(u'parameters_pvmodule', 'mbvoc', 'Mbvoc')

        # Adding field 'PVModule.Mbvoc'
        db.alter_column(u'parameters_pvmodule', 'Mbvoc',
                      self.gf('django.db.models.fields.FloatField')(default=0))

        # Deleting field 'PVModule.bvoc0'
        db.rename_column(u'parameters_pvmodule', 'bvoc0', 'Bvoco')

        # Adding field 'PVModule.Bvoco'
        db.alter_column(u'parameters_pvmodule', 'Bvoco',
                      self.gf('django.db.models.fields.FloatField')(default=0))

        # Deleting field 'PVModule.a1'
        db.rename_column(u'parameters_pvmodule', 'a1', 'A1')

        # Deleting field 'PVModule.a0'
        db.rename_column(u'parameters_pvmodule', 'a0', 'A0')

        # Deleting field 'PVModule.a3'
        db.rename_column(u'parameters_pvmodule', 'a3', 'A3')

        # Deleting field 'PVModule.a2'
        db.rename_column(u'parameters_pvmodule', 'a2', 'A2')

        # Deleting field 'PVModule.fd'
        db.rename_column(u'parameters_pvmodule', 'fd', 'FD')

        # Adding field 'PVModule.FD'
        db.alter_column(u'parameters_pvmodule', 'FD',
                      self.gf('django.db.models.fields.FloatField')(default=0))

        # Deleting field 'PVModule.a4'
        db.rename_column(u'parameters_pvmodule', 'a4', 'A4')

        # Adding field 'PVModule.A0'
        db.alter_column(u'parameters_pvmodule', 'A0',
                      self.gf('django.db.models.fields.FloatField')(default=0))

        # Adding field 'PVModule.A1'
        db.alter_column(u'parameters_pvmodule', 'A1',
                      self.gf('django.db.models.fields.FloatField')(default=0))

        # Adding field 'PVModule.A2'
        db.alter_column(u'parameters_pvmodule', 'A2',
                      self.gf('django.db.models.fields.FloatField')(default=0))

        # Adding field 'PVModule.A3'
        db.alter_column(u'parameters_pvmodule', 'A3',
                      self.gf('django.db.models.fields.FloatField')(default=0))

        # Adding field 'PVModule.A4'
        db.alter_column(u'parameters_pvmodule', 'A4',
                      self.gf('django.db.models.fields.FloatField')(default=0))

        # Deleting field 'PVModule.aisc'
        db.rename_column(u'parameters_pvmodule', 'aisc', 'Aisc')

        # Adding field 'PVModule.Aisc'
        db.alter_column(u'parameters_pvmodule', 'Aisc',
                      self.gf('django.db.models.fields.FloatField')(default=0))

        # Deleting field 'PVModule.ixx0'
        db.rename_column(u'parameters_pvmodule', 'ixx0', 'IXXO')

        # Adding field 'PVModule.IXXO'
        db.alter_column(u'parameters_pvmodule', 'IXXO',
                      self.gf('django.db.models.fields.FloatField')(default=0))

        # Deleting field 'PVModule.vintage_estimated'
        db.delete_column(u'parameters_pvmodule', 'vintage_estimated')

        # Adding field 'PVModule.C4'
        db.alter_column(u'parameters_pvmodule', 'C4',
                      self.gf('django.db.models.fields.FloatField')(default=0))

        # Adding field 'PVModule.C5'
        db.alter_column(u'parameters_pvmodule', 'C5',
                      self.gf('django.db.models.fields.FloatField')(default=0))

        # Adding field 'PVModule.C6'
        db.alter_column(u'parameters_pvmodule', 'C6',
                      self.gf('django.db.models.fields.FloatField')(default=0))

        # Adding field 'PVModule.C7'
        db.alter_column(u'parameters_pvmodule', 'C7',
                      self.gf('django.db.models.fields.FloatField')(default=0))

        # Adding unique constraint on 'PVModule', fields ['Name', 'Vintage', 'Notes']
        db.create_unique(u'parameters_pvmodule', ['Name', 'Vintage', 'Notes'])


    def backwards(self, orm):
        # Removing unique constraint on 'PVModule', fields ['Name', 'Vintage', 'Notes']
        db.delete_unique(u'parameters_pvmodule', ['Name', 'Vintage', 'Notes'])

        # Deleting field 'PVModule.DTC'
        db.rename_column(u'parameters_pvmodule', 'DTC', 'dt')

        # Adding field 'PVModule.dt'
        db.alter_column(u'parameters_pvmodule', 'dt',
                      self.gf('django.db.models.fields.FloatField')(default=-999))

        # Deleting field 'PVModule.Isco'
        db.rename_column(u'parameters_pvmodule', 'Isco', 'isc0')

        # Deleting field 'PVModule.Voco'
        db.rename_column(u'parameters_pvmodule', 'Voco', 'voc0')

        # Deleting field 'PVModule.Impo'
        db.rename_column(u'parameters_pvmodule', 'Impo', 'imp0')

        # Deleting field 'PVModule.Vmpo'
        db.rename_column(u'parameters_pvmodule', 'Vmpo', 'vmp0')

        # Adding field 'PVModule.imp0'
        db.alter_column(u'parameters_pvmodule', 'imp0',
                      self.gf('django.db.models.fields.FloatField')(default=-999))

        # Deleting field 'PVModule.Area'
        db.rename_column(u'parameters_pvmodule', 'Area', 'area')

        # Adding field 'PVModule.area'
        db.alter_column(u'parameters_pvmodule', 'area',
                      self.gf('django.db.models.fields.FloatField')(default=-999))

        # Deleting field 'PVModule.Bvoco'
        db.rename_column(u'parameters_pvmodule', 'Bvoco')

        # Deleting field 'PVModule.Mbvoc'
        db.rename_column(u'parameters_pvmodule', 'Mbvoc')

        # Deleting field 'PVModule.Bvmpo'
        db.rename_column(u'parameters_pvmodule', 'Bvmpo', 'bvmp0')

        # Deleting field 'PVModule.Mbvmp'
        db.rename_column(u'parameters_pvmodule', 'Mbvmp', 'mbvmp')

        # Adding field 'PVModule.bvmp0'
        db.alter_column(u'parameters_pvmodule', 'bvmp0',
                      self.gf('django.db.models.fields.FloatField')(default=-999))

        # Adding field 'PVModule.a'
        db.alter_column(u'parameters_pvmodule', 'a',
                      self.gf('django.db.models.fields.FloatField')(default=-999))

        # Adding field 'PVModule.mbvmp'
        db.alter_column(u'parameters_pvmodule', 'mbvmp',
                      self.gf('django.db.models.fields.FloatField')(default=-999))

        # Deleting field 'PVModule.Material'
        db.rename_column(u'parameters_pvmodule', 'Material')

        # Adding field 'PVModule.material'
        db.alter_column(u'parameters_pvmodule', 'material',
                      self.gf('django.db.models.fields.IntegerField')(default=10))

        # Deleting field 'PVModule.C0'
        db.rename_column(u'parameters_pvmodule', 'C0', 'c0')

        # Deleting field 'PVModule.C1'
        db.rename_column(u'parameters_pvmodule', 'C1', 'c1')

        # Deleting field 'PVModule.N'
        db.rename_column(u'parameters_pvmodule', 'N', 'n')

        # Deleting field 'PVModule.C2'
        db.rename_column(u'parameters_pvmodule', 'C2', 'c2')

        # Deleting field 'PVModule.C3'
        db.rename_column(u'parameters_pvmodule', 'C3', 'c3')

        # Deleting field 'PVModule.A0'
        db.rename_column(u'parameters_pvmodule', 'A0', 'a0')

        # Deleting field 'PVModule.A1'
        db.rename_column(u'parameters_pvmodule', 'A1', 'a1')

        # Deleting field 'PVModule.A2'
        db.rename_column(u'parameters_pvmodule', 'A2', 'a2')

        # Deleting field 'PVModule.A3'
        db.rename_column(u'parameters_pvmodule', 'A3', 'a3')

        # Deleting field 'PVModule.A4'
        db.rename_column(u'parameters_pvmodule', 'A4', 'a4')

        # Deleting field 'PVModule.B0'
        db.rename_column(u'parameters_pvmodule', 'B0', 'b0')

        # Deleting field 'PVModule.B1'
        db.rename_column(u'parameters_pvmodule', 'B1', 'b1')

        # Deleting field 'PVModule.B2'
        db.rename_column(u'parameters_pvmodule', 'B2', 'b2')

        # Deleting field 'PVModule.B3'
        db.rename_column(u'parameters_pvmodule', 'B3', 'b3')

        # Deleting field 'PVModule.B4'
        db.rename_column(u'parameters_pvmodule', 'B4', 'b4')

        # Deleting field 'PVModule.B5'
        db.rename_column(u'parameters_pvmodule', 'B5', 'b5')

        # Deleting field 'PVModule.FD'
        db.rename_column(u'parameters_pvmodule', 'FD', 'fd')

        # Deleting field 'PVModule.A'
        db.rename_column(u'parameters_pvmodule', 'A', 'a')

        # Deleting field 'PVModule.B'
        db.rename_column(u'parameters_pvmodule', 'B', 'b')

        # Deleting field 'PVModule.C4'
        db.rename_column(u'parameters_pvmodule', 'C4', 'c4')

        # Deleting field 'PVModule.C5'
        db.rename_column(u'parameters_pvmodule', 'C5', 'c5')

        # Deleting field 'PVModule.IXO'
        db.rename_column(u'parameters_pvmodule', 'IXO', 'ix0')

        # Deleting field 'PVModule.IXXO'
        db.rename_column(u'parameters_pvmodule', 'IXXO', 'ixx0')

        # Deleting field 'PVModule.C6'
        db.rename_column(u'parameters_pvmodule', 'C6', 'c6')

        # Deleting field 'PVModule.C7'
        db.rename_column(u'parameters_pvmodule', 'C7', 'c7')

        # Deleting field 'PVModule.Notes'
        db.rename_column(u'parameters_pvmodule', 'Notes', 'notes')

        # Adding field 'PVModule.c3'
        db.alter_column(u'parameters_pvmodule', 'c3',
                      self.gf('django.db.models.fields.FloatField')(default=-999))

        # Adding field 'PVModule.c2'
        db.alter_column(u'parameters_pvmodule', 'c2',
                      self.gf('django.db.models.fields.FloatField')(default=-999),
                      keep_default=False)

        # Adding field 'PVModule.c1'
        db.alter_column(u'parameters_pvmodule', 'c1',
                      self.gf('django.db.models.fields.FloatField')(default=-999),
                      keep_default=False)

        # Adding field 'PVModule.c0'
        db.alter_column(u'parameters_pvmodule', 'c0',
                      self.gf('django.db.models.fields.FloatField')(default=-999),
                      keep_default=False)

        # Adding field 'PVModule.c7'
        db.alter_column(u'parameters_pvmodule', 'c7',
                      self.gf('django.db.models.fields.FloatField')(default=-999),
                      keep_default=False)

        # Adding field 'PVModule.c6'
        db.alter_column(u'parameters_pvmodule', 'c6',
                      self.gf('django.db.models.fields.FloatField')(default=-999),
                      keep_default=False)

        # Adding field 'PVModule.c5'
        db.alter_column(u'parameters_pvmodule', 'c5',
                      self.gf('django.db.models.fields.FloatField')(default=-999),
                      keep_default=False)

        # Adding field 'PVModule.c4'
        db.alter_column(u'parameters_pvmodule', 'c4',
                      self.gf('django.db.models.fields.FloatField')(default=-999),
                      keep_default=False)

        # Adding field 'PVModule.b'
        db.alter_column(u'parameters_pvmodule', 'b',
                      self.gf('django.db.models.fields.FloatField')(default=-999),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PVModule.name'
        raise RuntimeError("Cannot reverse this migration. 'PVModule.name' and its values cannot be restored.")

        # Deleting field 'PVModule.Name'
        db.rename_column(u'parameters_pvmodule', 'Name', 'name')
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PVModule.name'
        db.alter_column(u'parameters_pvmodule', 'name',
                      self.gf('django.db.models.fields.CharField')(max_length=100),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'PVModule.notes'
        raise RuntimeError("Cannot reverse this migration. 'PVModule.notes' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PVModule.notes'
        db.alter_column(u'parameters_pvmodule', 'notes',
                      self.gf('django.db.models.fields.CharField')(max_length=100),
                      keep_default=False)

        # Deleting field 'PVModule.Aimp'
        db.rename_column(u'parameters_pvmodule', 'Aimp', 'aimp')

        # Adding field 'PVModule.aimp'
        db.alter_column(u'parameters_pvmodule', 'aimp',
                      self.gf('django.db.models.fields.FloatField')(default=-999))

        # Adding field 'PVModule.n'
        db.alter_column(u'parameters_pvmodule', 'n',
                      self.gf('django.db.models.fields.FloatField')(default=-999))

        # Adding field 'PVModule.ix0'
        db.alter_column(u'parameters_pvmodule', 'ix0',
                      self.gf('django.db.models.fields.FloatField')(default=-999))

        # Adding field 'PVModule.isc0'
        db.alter_column(u'parameters_pvmodule', 'isc0',
                      self.gf('django.db.models.fields.FloatField')(default=-999))

        # Adding field 'PVModule.b4'
        db.alter_column(u'parameters_pvmodule', 'b4',
                      self.gf('django.db.models.fields.FloatField')(default=-999))

        # Adding field 'PVModule.b5'
        db.alter_column(u'parameters_pvmodule', 'b5',
                      self.gf('django.db.models.fields.FloatField')(default=-999))

        # Adding field 'PVModule.b0'
        db.alter_column(u'parameters_pvmodule', 'b0',
                      self.gf('django.db.models.fields.FloatField')(default=-999))

        # Adding field 'PVModule.b1'
        db.alter_column(u'parameters_pvmodule', 'b1',
                      self.gf('django.db.models.fields.FloatField')(default=-999))

        # Adding field 'PVModule.b2'
        db.alter_column(u'parameters_pvmodule', 'b2',
                      self.gf('django.db.models.fields.FloatField')(default=-999))

        # Adding field 'PVModule.b3'
        db.alter_column(u'parameters_pvmodule', 'b3',
                      self.gf('django.db.models.fields.FloatField')(default=-999))

        # Adding field 'PVModule.vmp0'
        db.alter_column(u'parameters_pvmodule', 'vmp0',
                      self.gf('django.db.models.fields.FloatField')(default=-999))

        # Deleting field 'PVModule.Vintage'
        db.rename_column(u'parameters_pvmodule', 'Vintage', 'vintage')

        # Adding field 'PVModule.vintage'
        db.alter_column(u'parameters_pvmodule', 'vintage',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(1999, 1, 1, 0, 0)))

        # Adding field 'PVModule.voc0'
        db.alter_column(u'parameters_pvmodule', 'voc0',
                      self.gf('django.db.models.fields.FloatField')(default=-999))

        # Deleting field 'PVModule.Cells_in_Series'
        db.rename_column(u'parameters_pvmodule', 'Cells_in_Series', 'cells_in_series')

        # Deleting field 'PVModule.Parallel_Strings'
        db.rename_column(u'parameters_pvmodule', 'Parallel_Strings', 'parallel_strings')

        # Adding field 'PVModule.parallel_strings'
        db.alter_column(u'parameters_pvmodule', 'parallel_strings',
                      self.gf('django.db.models.fields.IntegerField')(default=-999))

        # Adding field 'PVModule.cells_in_series'
        db.alter_column(u'parameters_pvmodule', 'cells_in_series',
                      self.gf('django.db.models.fields.IntegerField')(default=-999))

        # Adding field 'PVModule.mbvoc'
        db.alter_column(u'parameters_pvmodule', 'mbvoc',
                      self.gf('django.db.models.fields.FloatField')(default=-999))

        # Adding field 'PVModule.bvoc0'
        db.alter_column(u'parameters_pvmodule', 'bvoc0',
                      self.gf('django.db.models.fields.FloatField')(default=-999))

        # Adding field 'PVModule.a1'
        db.alter_column(u'parameters_pvmodule', 'a1',
                      self.gf('django.db.models.fields.FloatField')(default=-999))

        # Adding field 'PVModule.a0'
        db.alter_column(u'parameters_pvmodule', 'a0',
                      self.gf('django.db.models.fields.FloatField')(default=-999))

        # Adding field 'PVModule.a3'
        db.alter_column(u'parameters_pvmodule', 'a3',
                      self.gf('django.db.models.fields.FloatField')(default=-999))

        # Adding field 'PVModule.a2'
        db.alter_column(u'parameters_pvmodule', 'a2',
                      self.gf('django.db.models.fields.FloatField')(default=-999))

        # Adding field 'PVModule.fd'
        db.alter_column(u'parameters_pvmodule', 'fd',
                      self.gf('django.db.models.fields.FloatField')(default=-999))

        # Adding field 'PVModule.a4'
        db.alter_column(u'parameters_pvmodule', 'a4',
                      self.gf('django.db.models.fields.FloatField')(default=-999))

        # Deleting field 'PVModule.Aisc'
        db.rename_column(u'parameters_pvmodule', 'Aisc', 'aisc')

        # Adding field 'PVModule.aisc'
        db.alter_column(u'parameters_pvmodule', 'aisc',
                      self.gf('django.db.models.fields.FloatField')(default=-999))

        # Adding field 'PVModule.ixx0'
        db.alter_column(u'parameters_pvmodule', 'ixx0',
                      self.gf('django.db.models.fields.FloatField')(default=-999))

        # Adding field 'PVModule.vintage_estimated'
        db.add_column(u'parameters_pvmodule', 'vintage_estimated',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding unique constraint on 'PVModule', fields ['name', 'vintage', 'vintage_estimated', 'notes']
        db.create_unique(u'parameters_pvmodule', ['name', 'vintage', 'vintage_estimated', 'notes'])


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
            'C4': ('django.db.models.fields.FloatField', [], {}),
            'C5': ('django.db.models.fields.FloatField', [], {}),
            'C6': ('django.db.models.fields.FloatField', [], {}),
            'C7': ('django.db.models.fields.FloatField', [], {}),
            'Cells_in_Series': ('django.db.models.fields.IntegerField', [], {}),
            'DTC': ('django.db.models.fields.FloatField', [], {}),
            'FD': ('django.db.models.fields.FloatField', [], {}),
            'IXO': ('django.db.models.fields.FloatField', [], {}),
            'IXXO': ('django.db.models.fields.FloatField', [], {}),
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['parameters']