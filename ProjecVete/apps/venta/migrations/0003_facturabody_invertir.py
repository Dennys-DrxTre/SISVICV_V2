# Generated by Django 3.0.6 on 2020-06-27 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0002_auto_20200523_1007'),
    ]

    operations = [
        migrations.AddField(
            model_name='facturabody',
            name='invertir',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
