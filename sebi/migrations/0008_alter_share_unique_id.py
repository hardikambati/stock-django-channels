# Generated by Django 3.2.7 on 2023-01-19 13:51

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('sebi', '0007_alter_share_unique_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='share',
            name='unique_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
