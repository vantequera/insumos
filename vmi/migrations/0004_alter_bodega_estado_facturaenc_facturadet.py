# Generated by Django 4.0.3 on 2022-04-11 21:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vmi', '0003_alter_ciudad_codigo_dane_ciudad_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bodega',
            name='estado',
            field=models.CharField(choices=[('Activo', 'Activo'), ('Inhabilitado', 'Inhabilitado'), ('Atrasado', 'Atrasado')], default='A', max_length=20, verbose_name='Esatdo de la Bodega'),
        ),
        migrations.CreateModel(
            name='FacturaEnc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_crea', models.DateTimeField(auto_now_add=True)),
                ('fecha_modifica', models.DateTimeField(auto_now=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('sub_total', models.FloatField(default=0)),
                ('descuento', models.FloatField(default=0)),
                ('total', models.FloatField(default=0)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vmi.proveedor')),
            ],
            options={
                'verbose_name': 'Encabezado de Factura',
                'verbose_name_plural': 'Encabezados de Facturas',
            },
        ),
        migrations.CreateModel(
            name='FacturaDet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_crea', models.DateTimeField(auto_now_add=True)),
                ('fecha_modifica', models.DateTimeField(auto_now=True)),
                ('cantidad', models.BigIntegerField(default=0)),
                ('precio', models.FloatField(default=0)),
                ('sub_total', models.FloatField(default=0)),
                ('descuento', models.FloatField(default=0)),
                ('total', models.FloatField(default=0)),
                ('factura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vmi.facturaenc')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vmi.referencia')),
            ],
            options={
                'verbose_name': 'Detalle de Factura',
                'verbose_name_plural': 'Detalles de Facturas',
            },
        ),
    ]
