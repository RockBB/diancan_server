# Generated by Django 2.1.7 on 2019-12-27 14:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20191227_1826'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userfood',
            name='out_time',
        ),
    ]
