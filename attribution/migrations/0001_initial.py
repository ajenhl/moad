# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Date'
        db.create_table(u'attribution_date', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('assertion', self.gf('django.db.models.fields.related.ForeignKey')(related_name='dates', to=orm['attribution.PropertyAssertion'])),
        ))
        db.send_create_signal(u'attribution', ['Date'])

        # Adding model 'Identifier'
        db.create_table(u'attribution_identifier', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('assertion', self.gf('django.db.models.fields.related.ForeignKey')(related_name='identifiers', to=orm['attribution.PropertyAssertion'])),
        ))
        db.send_create_signal(u'attribution', ['Identifier'])

        # Adding model 'Person'
        db.create_table(u'attribution_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('date', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'attribution', ['Person'])

        # Adding model 'Source'
        db.create_table(u'attribution_source', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('date', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('abbreviation', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
        ))
        db.send_create_signal(u'attribution', ['Source'])

        # Adding model 'TextIdentifierCache'
        db.create_table(u'attribution_textidentifiercache', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.related.OneToOneField')(related_name='cached_identifier', unique=True, to=orm['attribution.Text'])),
            ('identifier', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'attribution', ['TextIdentifierCache'])

        # Adding model 'Text'
        db.create_table(u'attribution_text', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'attribution', ['Text'])

        # Adding model 'Title'
        db.create_table(u'attribution_title', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('assertion', self.gf('django.db.models.fields.related.ForeignKey')(related_name='titles', to=orm['attribution.PropertyAssertion'])),
        ))
        db.send_create_signal(u'attribution', ['Title'])

        # Adding model 'PropertyAssertion'
        db.create_table(u'attribution_propertyassertion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(related_name='assertions', to=orm['attribution.Source'])),
            ('source_detail', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('argument', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_preferred', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'attribution', ['PropertyAssertion'])

        # Adding M2M table for field texts on 'PropertyAssertion'
        m2m_table_name = db.shorten_name(u'attribution_propertyassertion_texts')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('propertyassertion', models.ForeignKey(orm[u'attribution.propertyassertion'], null=False)),
            ('text', models.ForeignKey(orm[u'attribution.text'], null=False))
        ))
        db.create_unique(m2m_table_name, ['propertyassertion_id', 'text_id'])

        # Adding M2M table for field authors on 'PropertyAssertion'
        m2m_table_name = db.shorten_name(u'attribution_propertyassertion_authors')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('propertyassertion', models.ForeignKey(orm[u'attribution.propertyassertion'], null=False)),
            ('person', models.ForeignKey(orm[u'attribution.person'], null=False))
        ))
        db.create_unique(m2m_table_name, ['propertyassertion_id', 'person_id'])

        # Adding M2M table for field translators on 'PropertyAssertion'
        m2m_table_name = db.shorten_name(u'attribution_propertyassertion_translators')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('propertyassertion', models.ForeignKey(orm[u'attribution.propertyassertion'], null=False)),
            ('person', models.ForeignKey(orm[u'attribution.person'], null=False))
        ))
        db.create_unique(m2m_table_name, ['propertyassertion_id', 'person_id'])


    def backwards(self, orm):
        # Deleting model 'Date'
        db.delete_table(u'attribution_date')

        # Deleting model 'Identifier'
        db.delete_table(u'attribution_identifier')

        # Deleting model 'Person'
        db.delete_table(u'attribution_person')

        # Deleting model 'Source'
        db.delete_table(u'attribution_source')

        # Deleting model 'TextIdentifierCache'
        db.delete_table(u'attribution_textidentifiercache')

        # Deleting model 'Text'
        db.delete_table(u'attribution_text')

        # Deleting model 'Title'
        db.delete_table(u'attribution_title')

        # Deleting model 'PropertyAssertion'
        db.delete_table(u'attribution_propertyassertion')

        # Removing M2M table for field texts on 'PropertyAssertion'
        db.delete_table(db.shorten_name(u'attribution_propertyassertion_texts'))

        # Removing M2M table for field authors on 'PropertyAssertion'
        db.delete_table(db.shorten_name(u'attribution_propertyassertion_authors'))

        # Removing M2M table for field translators on 'PropertyAssertion'
        db.delete_table(db.shorten_name(u'attribution_propertyassertion_translators'))


    models = {
        u'attribution.date': {
            'Meta': {'object_name': 'Date'},
            'assertion': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dates'", 'to': u"orm['attribution.PropertyAssertion']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'})
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
            'name': ('django.db.models.fields.TextField', [], {})
        },
        u'attribution.text': {
            'Meta': {'object_name': 'Text'},
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