# Generated by Django 3.0.6 on 2020-06-27 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inv', '0002_remove_producto_departamento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='stock',
            field=models.IntegerField(verbose_name='Cantidad del Producto'),
        ),
    ]