# Generated by Django 4.0.3 on 2022-03-24 12:15

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('vmi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='fechaFactura',
            field=models.DateTimeField(verbose_name=datetime.datetime(2022, 3, 24, 12, 15, 35, 15689, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='movinventario',
            name='fechaMov',
            field=models.DateTimeField(verbose_name=datetime.datetime(2022, 3, 24, 12, 15, 35, 18149, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='fecha_pedido',
            field=models.DateTimeField(verbose_name=datetime.datetime(2022, 3, 24, 12, 15, 35, 16570, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='pedidosmov',
            name='fecha_pedido',
            field=models.DateTimeField(verbose_name=datetime.datetime(2022, 3, 24, 12, 15, 35, 17078, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='fecha_creacion',
            field=models.DateTimeField(verbose_name=datetime.datetime(2022, 3, 24, 12, 15, 35, 13088, tzinfo=utc)),
        ),
    ]