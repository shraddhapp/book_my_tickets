# Generated by Django 3.2.9 on 2021-11-28 19:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movietheatreshow',
            name='city',
        ),
    ]
