# Generated by Django 3.1.4 on 2021-05-21 05:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20210521_0535'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='color',
            name='slug',
        ),
    ]
