# Generated by Django 2.0.6 on 2020-05-03 22:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0006_auto_20200503_2227'),
    ]

    operations = [
        migrations.RenameField(
            model_name='representation',
            old_name='image_file',
            new_name='image',
        ),
        migrations.RemoveField(
            model_name='representation',
            name='image_url',
        ),
    ]
