# Generated by Django 2.1.4 on 2020-04-19 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livedash', '0002_auto_20200420_0114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backgroundimagesstore',
            name='image',
            field=models.CharField(max_length=100),
        ),
    ]
