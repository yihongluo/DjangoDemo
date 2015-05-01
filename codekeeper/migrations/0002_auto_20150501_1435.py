# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codekeeper', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=128)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='person',
            options={'verbose_name_plural': 'people'},
        ),
        migrations.AlterField(
            model_name='snippet',
            name='tags',
            field=models.ManyToManyField(to='codekeeper.Tag', blank=True, null=True, default='DEFAULT'),
        ),
        migrations.AlterField(
            model_name='snippet',
            name='title',
            field=models.CharField(max_length=256, blank=True, null=True, default='DEFAULT'),
        ),
        migrations.AddField(
            model_name='snippet',
            name='language',
            field=models.ForeignKey(to='codekeeper.Language', default=0),
            preserve_default=False,
        ),
    ]
