# Generated by Django 3.2.7 on 2021-11-19 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_a', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock', models.ManyToManyField(blank=True, to='stock_a.AllStock')),
            ],
        ),
    ]
