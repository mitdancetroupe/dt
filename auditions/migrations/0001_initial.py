# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PrefSheet'
        db.create_table('auditions_prefsheet', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('audition_number', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='prefsheets', to=orm['auth.User'])),
            ('conflicts', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('desired_dances', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('show', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shows.Show'])),
        ))
        db.send_create_signal('auditions', ['PrefSheet'])

        # Adding unique constraint on 'PrefSheet', fields ['user', 'show']
        db.create_unique('auditions_prefsheet', ['user_id', 'show_id'])

        # Adding unique constraint on 'PrefSheet', fields ['audition_number', 'show']
        db.create_unique('auditions_prefsheet', ['audition_number', 'show_id'])

        # Adding model 'Pref'
        db.create_table('auditions_pref', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('prefsheet', self.gf('django.db.models.fields.related.ForeignKey')(related_name='prefs', to=orm['auditions.PrefSheet'])),
            ('dance', self.gf('django.db.models.fields.related.ForeignKey')(related_name='prefs', to=orm['shows.Dance'])),
            ('pref', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('auditions', ['Pref'])

        # Adding unique constraint on 'Pref', fields ['prefsheet', 'dance']
        db.create_unique('auditions_pref', ['prefsheet_id', 'dance_id'])

        # Adding unique constraint on 'Pref', fields ['prefsheet', 'pref']
        db.create_unique('auditions_pref', ['prefsheet_id', 'pref'])


    def backwards(self, orm):
        # Removing unique constraint on 'Pref', fields ['prefsheet', 'pref']
        db.delete_unique('auditions_pref', ['prefsheet_id', 'pref'])

        # Removing unique constraint on 'Pref', fields ['prefsheet', 'dance']
        db.delete_unique('auditions_pref', ['prefsheet_id', 'dance_id'])

        # Removing unique constraint on 'PrefSheet', fields ['audition_number', 'show']
        db.delete_unique('auditions_prefsheet', ['audition_number', 'show_id'])

        # Removing unique constraint on 'PrefSheet', fields ['user', 'show']
        db.delete_unique('auditions_prefsheet', ['user_id', 'show_id'])

        # Deleting model 'PrefSheet'
        db.delete_table('auditions_prefsheet')

        # Deleting model 'Pref'
        db.delete_table('auditions_pref')


    models = {
        'auditions.pref': {
            'Meta': {'ordering': "('prefsheet', 'pref')", 'unique_together': "(('prefsheet', 'dance'), ('prefsheet', 'pref'))", 'object_name': 'Pref'},
            'dance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'prefs'", 'to': "orm['shows.Dance']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pref': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'prefsheet': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'prefs'", 'to': "orm['auditions.PrefSheet']"})
        },
        'auditions.prefsheet': {
            'Meta': {'ordering': "('audition_number',)", 'unique_together': "(('user', 'show'), ('audition_number', 'show'))", 'object_name': 'PrefSheet'},
            'audition_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'conflicts': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'desired_dances': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'show': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shows.Show']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'prefsheets'", 'to': "orm['auth.User']"})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'shows.dance': {
            'Meta': {'object_name': 'Dance'},
            'choreographers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'choreographed'", 'blank': 'True', 'to': "orm['auth.User']"}),
            'dancers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'danced_in'", 'blank': 'True', 'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'show': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dances'", 'to': "orm['shows.Show']"}),
            'style': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'shows.show': {
            'Meta': {'ordering': "('-year', '-semester')", 'object_name': 'Show'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'prefsheets_open': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'semester': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['auditions']