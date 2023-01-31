# Generated by Django 3.2.7 on 2023-01-19 09:07

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('sebi', '0002_alter_share_unique_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='share',
            name='unique_id',
            field=models.CharField(default=uuid.UUID('70e5d86f-75e9-4235-8343-e05fc88809a0'), editable=False, max_length=255),
        ),
    ]