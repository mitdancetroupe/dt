# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Availability', fields ['prefsheet', 'time']
        db.delete_unique('auditions_availability', ['prefsheet_id', 'time_id'])

        # Removing unique constraint on 'Time', fields ['day', 'hour']
        db.delete_unique('auditions_time', ['day', 'hour'])

        # Deleting model 'Time'
        db.delete_table('auditions_time')

        # Deleting field 'Availability.time'
        db.delete_column('auditions_availability', 'time_id')

        # Adding field 'Availability.day'
        db.add_column('auditions_availability', 'day',
                      self.gf('django.db.models.fields.CharField')(default='m', max_length=12),
                      keep_default=False)

        # Adding field 'Availability.hour'
        db.add_column('auditions_availability', 'hour',
                      self.gf('django.db.models.fields.CharField')(default='0000', max_length=12),
                      keep_default=False)

        # Adding unique constraint on 'Availability', fields ['prefsheet', 'day', 'hour']
        db.create_unique('auditions_availability', ['prefsheet_id', 'day', 'hour'])


    def backwards(self, orm):
        # Removing unique constraint on 'Availability', fields ['prefsheet', 'day', 'hour']
        db.delete_unique('auditions_availability', ['prefsheet_id', 'day', 'hour'])

        # Adding model 'Time'
        db.create_table('auditions_time', (
            ('day', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('hour', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('auditions', ['Time'])

        # Adding unique constraint on 'Time', fields ['day', 'hour']
        db.create_unique('auditions_time', ['day', 'hour'])

        # Adding field 'Availability.time'
        db.add_column('auditions_availability', 'time',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['auditions.Time']),
                      keep_default=False)

        # Deleting field 'Availability.day'
        db.delete_column('auditions_availability', 'day')

        # Deleting field 'Availability.hour'
        db.delete_column('auditions_availability', 'hour')

        # Adding unique constraint on 'Availability', fields ['prefsheet', 'time']
        db.create_unique('auditions_availability', ['prefsheet_id', 'time_id'])


    models = {
        'auditions.availability': {
            'Meta': {'unique_together': "(('prefsheet', 'day', 'hour'),)", 'object_name': 'Availability'},
            'available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'day': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'hour': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prefsheet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auditions.PrefSheet']"})
        },
        'auditions.pref': {
            'Meta': {'ordering': "('prefsheet', 'pref')", 'unique_together': "(('prefsheet', 'dance'), ('prefsheet', 'pref'))", 'object_name': 'Pref'},
            'accepted': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'dance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'prefs'", 'to': "orm['shows.Dance']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pref': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'prefsheet': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'prefs'", 'to': "orm['auditions.PrefSheet']"}),
            'return_if_not_placed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'auditions.prefsheet': {
            'Meta': {'ordering': "('audition_number',)", 'unique_together': "(('user', 'show'), ('audition_number', 'show'))", 'object_name': 'PrefSheet'},
            'accepted_dances': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'audition_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'conflicts': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'desired_dances': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rejected_dances': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
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