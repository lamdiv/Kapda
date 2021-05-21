# Generated by Django 3.1.4 on 2021-05-21 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='type',
            name='slug',
        ),
        migrations.AlterField(
            model_name='product',
            name='color',
            field=models.ManyToManyField(blank=True, to='shop.Color'),
        ),
        migrations.AlterField(
            model_name='type',
            name='name',
            field=models.CharField(max_length=54),
        ),
    ]
