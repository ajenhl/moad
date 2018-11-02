# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Date',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Separate multiple names with ", "', max_length=500)),
                ('notes', models.TextField(blank=True)),
                ('sort_date', models.IntegerField(help_text=b'Year used for sorting purposes', null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Identifier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Separate multiple names with ", "', max_length=500)),
                ('notes', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Separate multiple names with ", "', max_length=500)),
                ('notes', models.TextField(blank=True)),
                ('sort_date', models.IntegerField(help_text=b'Year used for sorting purposes', null=True, blank=True)),
                ('date', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='PersonInvolvement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='PersonRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Separate multiple names with ", "', max_length=500)),
                ('notes', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PropertyAssertion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source_detail', models.TextField(blank=True)),
                ('argument', models.TextField(blank=True)),
                ('is_preferred', models.BooleanField(default=False)),
                ('people', models.ManyToManyField(to='attribution.Person', through='attribution.PersonInvolvement')),
            ],
            options={
                'ordering': ['source'],
                'verbose_name': 'assertion',
            },
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.TextField(blank=True)),
                ('name', models.TextField(help_text=b'Full bibliographic details')),
                ('date', models.CharField(help_text=b'Format: YYYY. Use the earliest date if there is a range', max_length=5)),
                ('abbreviation', models.CharField(help_text=b'Bibliographic reference, eg. "Nattier 1992"', unique=True, max_length=30)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'ordering': ['cached_identifier__identifier'],
            },
        ),
        migrations.CreateModel(
            name='TextIdentifierCache',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.TextField(blank=True)),
                ('text', models.OneToOneField(related_name='cached_identifier', to='attribution.Text')),
            ],
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Separate multiple names with ", "', max_length=500)),
                ('assertion', models.ForeignKey(related_name='titles', to='attribution.PropertyAssertion')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='propertyassertion',
            name='source',
            field=models.ForeignKey(related_name='assertions', to='attribution.Source'),
        ),
        migrations.AddField(
            model_name='propertyassertion',
            name='texts',
            field=models.ManyToManyField(related_name='assertions', to='attribution.Text'),
        ),
        migrations.AddField(
            model_name='personinvolvement',
            name='assertion',
            field=models.ForeignKey(related_name='person_involvements', to='attribution.PropertyAssertion'),
        ),
        migrations.AddField(
            model_name='personinvolvement',
            name='person',
            field=models.ForeignKey(related_name='involvements', to='attribution.Person'),
        ),
        migrations.AddField(
            model_name='personinvolvement',
            name='role',
            field=models.ForeignKey(related_name='involvements', to='attribution.PersonRole'),
        ),
        migrations.AddField(
            model_name='identifier',
            name='assertion',
            field=models.ForeignKey(related_name='identifiers', to='attribution.PropertyAssertion'),
        ),
        migrations.AddField(
            model_name='date',
            name='assertion',
            field=models.ForeignKey(related_name='dates', to='attribution.PropertyAssertion'),
        ),
    ]
