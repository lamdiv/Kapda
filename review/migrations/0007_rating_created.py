# Generated by Django 3.1.4 on 2021-07-01 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0006_auto_20210701_0747'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='created',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
