# Generated by Django 3.0.6 on 2012-11-01 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regmedic', '0002_auto_20200521_0620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consulta',
            name='frecar',
            field=models.IntegerField(verbose_name='Frecuencia Cardiaca'),
        ),
        migrations.AlterField(
            model_name='consulta',
            name='freres',
            field=models.IntegerField(verbose_name='Frecuencia Respiratoria'),
        ),
        migrations.AlterField(
            model_name='consulta',
            name='motivo',
            field=models.CharField(max_length=60, verbose_name='Motivo de Consulta'),
        ),
        migrations.AlterField(
            model_name='consulta',
            name='sintomas',
            field=models.CharField(max_length=80, verbose_name='Sintomas Presentados'),
        ),
        migrations.AlterField(
            model_name='consulta',
            name='temp',
            field=models.IntegerField(verbose_name='Temperatura'),
        ),
        migrations.AlterField(
            model_name='mascota',
            name='especie',
            field=models.CharField(max_length=50, verbose_name='especie'),
        ),
        migrations.AlterField(
            model_name='mascota',
            name='razam',
            field=models.CharField(max_length=50, verbose_name='raza'),
        ),
        migrations.AlterField(
            model_name='mascota',
            name='sexom',
            field=models.CharField(max_length=40, verbose_name='sexo'),
        ),
        migrations.AlterField(
            model_name='vacuna',
            name='nomva',
            field=models.CharField(max_length=25, verbose_name='Nombre de la Vacuna/s'),
        ),
    ]
