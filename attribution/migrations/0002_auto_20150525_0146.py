# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('attribution', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='propertyassertion',
            options={'ordering': ['source'], 'verbose_name': 'assertion', 'permissions': (('change_assertion_author', 'Can change the author of an assertion'), ('change_assertion_contributors', 'Can change contributors to an assertion'), ('change_assertion_status', 'Can change publication status'), ('change_published_items', 'Can change published items'))},
        ),
        migrations.AddField(
            model_name='person',
            name='author',
            field=models.ForeignKey(related_name='authored_persons', default=2, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='person',
            name='status',
            field=models.CharField(default=b'DR', max_length=2, choices=[(b'DR', b'Draft'), (b'PU', b'Published')]),
        ),
        migrations.AddField(
            model_name='personrole',
            name='status',
            field=models.CharField(default=b'DR', max_length=2, choices=[(b'DR', b'Draft'), (b'PU', b'Published')]),
        ),
        migrations.AddField(
            model_name='propertyassertion',
            name='author',
            field=models.ForeignKey(related_name='authored_assertions', default=2, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='propertyassertion',
            name='contributors',
            field=models.ManyToManyField(related_name='contributed_assertions', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='propertyassertion',
            name='created',
            field=models.DateField(default=datetime.datetime(2015, 5, 25, 1, 45, 48, 461032, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='propertyassertion',
            name='modified',
            field=models.DateField(default=datetime.datetime(2015, 5, 25, 1, 45, 56, 132107, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='propertyassertion',
            name='status',
            field=models.CharField(default=b'DR', max_length=2, choices=[(b'DR', b'Draft'), (b'PU', b'Published')]),
        ),
        migrations.AddField(
            model_name='source',
            name='author',
            field=models.ForeignKey(related_name='authored_sources', default=2, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='source',
            name='status',
            field=models.CharField(default=b'DR', max_length=2, choices=[(b'DR', b'Draft'), (b'PU', b'Published')]),
        ),
        migrations.AddField(
            model_name='text',
            name='author',
            field=models.ForeignKey(related_name='authored_texts', default=2, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='text',
            name='status',
            field=models.CharField(default=b'DR', max_length=2, choices=[(b'DR', b'Draft'), (b'PU', b'Published')]),
        ),
    ]
