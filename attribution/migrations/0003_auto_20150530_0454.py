# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attribution', '0002_auto_20150525_0146'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='textidentifiercache',
            name='text',
        ),
        migrations.AlterModelOptions(
            name='text',
            options={'ordering': ['identifier']},
        ),
        migrations.AddField(
            model_name='text',
            name='identifier',
            field=models.TextField(help_text=b'A derived field holding all of the identifiers asserted for this text.', blank=True),
        ),
        migrations.DeleteModel(
            name='TextIdentifierCache',
        ),
    ]
