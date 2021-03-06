# Generated by Django 3.2.4 on 2021-06-28 11:50

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Elevation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('rast', django.contrib.gis.db.models.fields.RasterField(srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Zipcode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=5)),
                ('poly', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
            ],
        ),
    ]
