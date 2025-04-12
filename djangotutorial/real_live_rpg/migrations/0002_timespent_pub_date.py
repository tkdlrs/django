# Generated by Django 5.1.7 on 2025-04-06 00:15

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('real_live_rpg', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='timespent',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published'),
            preserve_default=False,
        ),
    ]
