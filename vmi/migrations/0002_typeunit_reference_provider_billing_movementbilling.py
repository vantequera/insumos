# Generated by Django 4.0.3 on 2022-04-07 20:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vmi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeUnit',
            fields=[
                ('tipo_unidad', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('estado_unidad', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_ref', models.CharField(max_length=100)),
                ('codigo_ean8', models.CharField(max_length=8)),
                ('codigo_ean13', models.CharField(max_length=13)),
                ('codigo_ean128', models.CharField(max_length=50)),
                ('tipo_unida', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='vmi.typeunit')),
            ],
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_proveedor', models.CharField(max_length=200)),
                ('nit', models.CharField(max_length=15)),
                ('numero_tel_1', models.CharField(max_length=7)),
                ('numero_tel_cel', models.CharField(max_length=10)),
                ('correo', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('estado_proveedor', models.CharField(choices=[('A', 'Activo'), ('I', 'Inhabilitado'), ('C', 'Cancelado')], max_length=1)),
                ('ciudad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vmi.city')),
            ],
        ),
        migrations.CreateModel(
            name='Billing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_facturacion', models.DateTimeField()),
                ('concepto', models.CharField(max_length=100)),
                ('proveedor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vmi.provider')),
            ],
        ),
        migrations.CreateModel(
            name='MovementBilling',
            fields=[
                ('billing_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='vmi.billing')),
                ('cantidad_compra', models.DecimalField(decimal_places=3, max_digits=12)),
                ('referencia_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='vmi.reference')),
                ('unidad_compra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vmi.typeunit')),
            ],
            bases=('vmi.billing',),
        ),
    ]
