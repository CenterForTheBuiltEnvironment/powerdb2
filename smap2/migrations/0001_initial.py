# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django_hstore.hstore
import smap2.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuTag',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('display_name', models.CharField(help_text=b'Name to show for tag', max_length=64, null=True, db_index=True, blank=True)),
                ('tag_name', models.CharField(help_text=b'Actual name of the tag in sMAP', max_length=64, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='MenuValue',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('tag_val', models.TextField(help_text=b'value to set')),
                ('tag_name', models.ForeignKey(to='smap2.MenuTag')),
            ],
        ),
        migrations.CreateModel(
            name='Stream',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('uuid', models.CharField(unique=True, max_length=36, db_index=True)),
                ('metadata', django_hstore.hstore.DictionaryField(default=b'hstore(array[]::varchar[])')),
            ],
            options={
                'db_table': 'stream',
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('uuid', models.CharField(default=smap2.models.new_uuid, max_length=36)),
                ('url', models.CharField(default=b'', max_length=512, blank=True)),
                ('resource', models.CharField(default=b'/+', max_length=512)),
                ('key', models.CharField(default=smap2.models.new_key, max_length=36)),
                ('public', models.BooleanField(default=True, db_index=True)),
                ('description', models.CharField(max_length=256)),
                ('can_view', models.ManyToManyField(related_name='can_view', to=settings.AUTH_USER_MODEL, blank=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'subscription',
            },
        ),
        migrations.CreateModel(
            name='Tree',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('tree', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='stream',
            name='subscription',
            field=models.ForeignKey(to='smap2.Subscription'),
        ),
    ]
