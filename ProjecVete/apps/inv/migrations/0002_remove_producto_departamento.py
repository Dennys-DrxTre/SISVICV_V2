# Generated by Django 3.0.6 on 2020-05-23 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inv', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='departamento',
        ),
    ]
