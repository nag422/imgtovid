# Generated by Django 2.1.4 on 2020-04-19 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BackgroundImagesStore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to='livestreams/images')),
            ],
        ),
        migrations.CreateModel(
            name='DataStore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=100)),
                ('sourcetype', models.CharField(max_length=100)),
                ('data', models.CharField(max_length=100000)),
            ],
        ),
        migrations.CreateModel(
            name='ExcelFileStore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('excel', models.FileField(upload_to='livestreams/excels')),
                ('language', models.CharField(max_length=100)),
                ('sourcetype', models.CharField(max_length=100)),
                ('data', models.CharField(max_length=100)),
            ],
        ),
    ]