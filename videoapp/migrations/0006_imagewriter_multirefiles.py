# Generated by Django 2.1.4 on 2020-04-03 07:13

from django.db import migrations, models
import videoapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('videoapp', '0005_imagewriter_font'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagewriter',
            name='multirefiles',
            field=models.ImageField(default=0, upload_to=videoapp.models.get_upload_path),
            preserve_default=False,
        ),
    ]
