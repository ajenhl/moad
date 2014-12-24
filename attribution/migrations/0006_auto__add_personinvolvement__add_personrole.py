# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PersonInvolvement'
        db.create_table(u'attribution_personinvolvement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='involvements', to=orm['attribution.Person'])),
            ('assertion', self.gf('django.db.models.fields.related.ForeignKey')(related_name='person_involvements', to=orm['attribution.PropertyAssertion'])),
            ('role', self.gf('django.db.models.fields.related.ForeignKey')(related_name='involvements', to=orm['attribution.PersonRole'])),
        ))
        db.send_create_signal(u'attribution', ['PersonInvolvement'])

        # Adding model 'PersonRole'
        db.create_table(u'attribution_personrole', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'attribution', ['PersonRole'])


    def backwards(self, orm):
        # Deleting model 'PersonInvolvement'
        db.delete_table(u'attribution_personinvolvement')

        # Deleting model 'PersonRole'
        db.delete_table(u'attribution_personrole')


    models = {
        u'attribution.date': {
            'Meta': {'object_name': 'Date'},
            'assertion': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dates'", 'to': u"orm['attribution.PropertyAssertion']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'sort_date': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'attribution.identifier': {
            'Meta': {'object_name': 'Identifier'},
            'assertion': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'identifiers'", 'to': u"orm['attribution.PropertyAssertion']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'attribution.person': {
            'Meta': {'ordering': "['name']", 'object_name': 'Person'},
            'date': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'sort_date': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'attribution.personinvolvement': {
            'Meta': {'object_name': 'PersonInvolvement'},
            'assertion': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'person_involvements'", 'to': u"orm['attribution.PropertyAssertion']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'involvements'", 'to': u"orm['attribution.Person']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'involvements'", 'to': u"orm['attribution.PersonRole']"})
        },
        u'attribution.personrole': {
            'Meta': {'object_name': 'PersonRole'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'attribution.propertyassertion': {
            'Meta': {'ordering': "['source']", 'object_name': 'PropertyAssertion'},
            'argument': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'authored'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['attribution.Person']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_preferred': ('django.db.models.fields.BooleanField', [], {}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assertions'", 'to': u"orm['attribution.Source']"}),
            'source_detail': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'texts': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'assertions'", 'symmetrical': 'False', 'to': u"orm['attribution.Text']"}),
            'translators': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'translated'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['attribution.Person']"})
        },
        u'attribution.source': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Source'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'date': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'attribution.text': {
            'Meta': {'ordering': "['cached_identifier__identifier']", 'object_name': 'Text'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'attribution.textidentifiercache': {
            'Meta': {'object_name': 'TextIdentifierCache'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'text': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'cached_identifier'", 'unique': 'True', 'to': u"orm['attribution.Text']"})
        },
        u'attribution.title': {
            'Meta': {'object_name': 'Title'},
            'assertion': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'titles'", 'to': u"orm['attribution.PropertyAssertion']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        }
    }

    complete_apps = ['attribution']