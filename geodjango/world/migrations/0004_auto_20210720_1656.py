# Generated by Django 3.2.5 on 2021-07-20 11:26

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0003_sentinel'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChangeOutputsPNG',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('file', models.FileField(upload_to='outputs/change_img/%Y/%m/%d')),
                ('uploaded_date', models.DateField(blank=True, default=datetime.date.today)),
                ('sentinel_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='world.sentinel')),
            ],
        ),
        migrations.DeleteModel(
            name='WorldBorder',
        ),
        migrations.DeleteModel(
            name='Zipcode',
        ),
    ]
