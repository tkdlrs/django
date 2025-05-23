# Generated by Django 5.1.7 on 2025-04-01 00:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_name', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='TimeSpent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(verbose_name='Training session start')),
                ('end_time', models.DateTimeField(verbose_name='Training session end')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='real_live_rpg.skill')),
            ],
        ),
    ]
