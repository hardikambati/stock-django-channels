# Generated by Django 3.2.7 on 2023-01-31 12:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0010_auto_20230124_1245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='intraday',
            name='valid_till',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 31, 3, 30, 0, 80163)),
        ),
    ]
