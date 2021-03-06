# Generated by Django 4.0.3 on 2022-03-24 12:50

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('vmi', '0003_alter_factura_fechafactura_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='fechaFactura',
            field=models.DateTimeField(verbose_name=datetime.datetime(2022, 3, 24, 12, 50, 7, 831784, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='movinventario',
            name='fechaMov',
            field=models.DateTimeField(verbose_name=datetime.datetime(2022, 3, 24, 12, 50, 7, 833710, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='fecha_pedido',
            field=models.DateTimeField(verbose_name=datetime.datetime(2022, 3, 24, 12, 50, 7, 832366, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='pedidosmov',
            name='fecha_pedido',
            field=models.DateTimeField(verbose_name=datetime.datetime(2022, 3, 24, 12, 50, 7, 832731, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='fecha_creacion',
            field=models.DateTimeField(verbose_name=datetime.datetime(2022, 3, 24, 12, 50, 7, 829518, tzinfo=utc)),
        ),
    ]
