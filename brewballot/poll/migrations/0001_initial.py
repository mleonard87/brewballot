# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('long_title', models.CharField(max_length=100)),
                ('short_title', models.CharField(max_length=30)),
                ('slug', models.SlugField()),
                ('is_active', models.BooleanField(default=False)),
                ('created_on', models.DateField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PollOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=10)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('poll', models.ForeignKey(to='poll.Poll')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sender_number', models.CharField(max_length=20)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('poll_option', models.ForeignKey(to='poll.PollOption')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([('poll_option', 'sender_number')]),
        ),
    ]
