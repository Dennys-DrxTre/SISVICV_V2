# Generated by Django 2.2.4 on 2020-05-21 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regmedic', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='apellido',
            field=models.CharField(default='', max_length=40, verbose_name='Apellidos'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cliente',
            name='co_fijo',
            field=models.CharField(blank=True, choices=[('0257', '0257'), ('0251', '0251')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='co_movil',
            field=models.CharField(blank=True, choices=[('0412', '0412'), ('0416', '0416'), ('0426', '0426'), ('0414', '0414'), ('0424', '0424')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='nombre',
            field=models.CharField(max_length=40, verbose_name='Nombres'),
        ),
    ]
