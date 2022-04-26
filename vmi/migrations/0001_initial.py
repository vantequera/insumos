# Generated by Django 4.0.3 on 2022-04-26 21:21

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bodega',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre de Bodega')),
                ('estado', models.CharField(choices=[('Activo', 'Activo'), ('Inhabilitado', 'Inhabilitado'), ('Atrasado', 'Atrasado')], default='A', max_length=20, verbose_name='Estado de la Bodega')),
            ],
        ),
        migrations.CreateModel(
            name='Ciudad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_ciudad', models.CharField(max_length=200, unique=True)),
                ('codigo_dane_ciudad', models.CharField(max_length=3)),
            ],
            options={
                'verbose_name': 'Ciudad',
                'verbose_name_plural': 'Ciudades',
                'ordering': ['nombre_ciudad'],
            },
        ),
        migrations.CreateModel(
            name='IngresoB_B',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True, verbose_name='Fecha y Hora')),
                ('transporte', models.CharField(max_length=100, verbose_name='Transportadora')),
                ('bodega_des', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='vmi.bodega', verbose_name='Bodega Destino')),
            ],
            options={
                'verbose_name': 'Ingreso Bodega - Bodega',
                'verbose_name_plural': 'Ingresos Bodegas - Bodegas',
            },
        ),
        migrations.CreateModel(
            name='IngresoP_B',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True, verbose_name='Fecha y Hora')),
                ('transporte', models.CharField(max_length=100, verbose_name='Transportadora')),
                ('factura_prov', models.CharField(max_length=50, verbose_name='Factura Recibida')),
                ('bodega_des', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='vmi.bodega', verbose_name='Bodega Destino')),
            ],
            options={
                'verbose_name': 'Ingreso Proveedor - Bodega',
                'verbose_name_plural': 'Ingresos Proveedores - Bodegas',
            },
        ),
        migrations.CreateModel(
            name='MovimientoTipo',
            fields=[
                ('nombre_mov', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('estado', models.CharField(choices=[('Entrada_Bodega', 'Entrada de Bodega'), ('Salida_Bodega', 'Salida de Bodega')], default='Entrada_Bodega', max_length=14)),
            ],
        ),
        migrations.CreateModel(
            name='Pais',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_pais', models.CharField(max_length=200)),
                ('codigo_pais', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Paises',
            },
        ),
        migrations.CreateModel(
            name='PedidoBB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_pedido', models.DateTimeField(auto_now_add=True)),
                ('concepto_general', models.CharField(max_length=255, verbose_name='Concepto de solicitud')),
                ('estado_solicitud', models.CharField(choices=[('SE', 'Solicitud Enviada'), ('AP', 'Aprobado'), ('CA', 'Cancelado'), ('RZ', 'Rechazado'), ('EN', 'Enviado'), ('RC', 'Recibido')], default='SE', max_length=2)),
                ('bodega_solicitada', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='vmi.bodega')),
            ],
            options={
                'verbose_name': 'Pedido Bodega a Bodega',
                'verbose_name_plural': 'Pedidos Bodega a Bodega',
            },
        ),
        migrations.CreateModel(
            name='PedidoPB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_pedido', models.DateTimeField(auto_now_add=True)),
                ('estado_solicitud', models.CharField(choices=[('SE', 'Solicitud Enviada'), ('AP', 'Aprobado'), ('CA', 'Cancelado'), ('RZ', 'Rechazado'), ('EN', 'Enviado'), ('RC', 'Recibido')], default='SE', max_length=2)),
                ('concepto_general', models.CharField(max_length=255, verbose_name='Concepto de solicitud')),
                ('cotizacion_recibida', models.FileField(upload_to='', verbose_name='Cotización Recibida')),
            ],
            options={
                'verbose_name': 'Pedido Proveedor a Bodega',
                'verbose_name_plural': 'Pedidos Proveedores a Bodega',
            },
        ),
        migrations.CreateModel(
            name='Periodo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateField(verbose_name='Inicio del corte')),
                ('fecha_fin', models.DateField(verbose_name='Fin del corte')),
                ('estado', models.BooleanField(default=True, verbose_name='Estado del periodo')),
            ],
        ),
        migrations.CreateModel(
            name='Referencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_ref', models.CharField(max_length=100)),
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('codigo_ean8', models.CharField(max_length=8, unique=True)),
                ('codigo_ean13', models.CharField(max_length=13, unique=True)),
                ('codigo_ean128', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SaldoHistorico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Salida',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True, verbose_name='Fecha y Hora')),
                ('transporte', models.CharField(max_length=100, verbose_name='Transportadora')),
                ('bodega_des', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='vmi.bodega', verbose_name='Bodega Destino')),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vmi.pedidobb', verbose_name='Pedido')),
            ],
            options={
                'verbose_name': 'Salida de Referencia',
                'verbose_name_plural': 'Salidas de Referencias',
            },
        ),
        migrations.CreateModel(
            name='UnidadTipo',
            fields=[
                ('tipo_unidad', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('estado_unidad', models.CharField(choices=[('A', 'Activo'), ('I', 'Inactivo')], default='A', max_length=1)),
                ('formula', models.DecimalField(decimal_places=6, max_digits=12)),
            ],
        ),
        migrations.CreateModel(
            name='Sede',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_sede', models.CharField(max_length=50, verbose_name='Nombre de Sede')),
                ('estado_sede', models.CharField(choices=[('O', 'Operativo'), ('F', 'Fuera de Servicio'), ('T', 'Traslado')], default='O', max_length=1, verbose_name='Estado de Sede')),
                ('direccion', models.CharField(default='none', max_length=50, verbose_name='Dirección')),
                ('municipio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vmi.ciudad')),
            ],
        ),
        migrations.CreateModel(
            name='SalidaRef',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empaque', models.CharField(choices=[('C', 'Cumple'), ('NC', 'No Cumple')], max_length=2, verbose_name='Empaque/Embalaje en General')),
                ('lote', models.CharField(max_length=8, verbose_name='Lote de paquete')),
                ('fecha_vencimiento', models.DateField(verbose_name='Fecha de Vencimiento')),
                ('cantidad', models.IntegerField(verbose_name='Cantidad Referencia Recibida')),
                ('observaciones', models.CharField(max_length=200, verbose_name='Observaciones')),
                ('integridad', models.CharField(choices=[('C', 'Cumple'), ('NC', 'No Cumple')], max_length=2, verbose_name='Integridad de la Referencia')),
                ('apariencia', models.CharField(choices=[('C', 'Cumple'), ('NC', 'No Cumple')], max_length=2, verbose_name='Apariencia de la Referencia')),
                ('temp', models.CharField(max_length=2, verbose_name='Temperatura de Almacenamiento')),
                ('referencia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vmi.referencia')),
                ('salida', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vmi.salida')),
                ('tipo_unidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vmi.unidadtipo')),
            ],
            options={
                'verbose_name': 'Referencia de Salida',
                'verbose_name_plural': 'Referencias de Salidas',
            },
        ),
        migrations.AddField(
            model_name='salida',
            name='sede_des',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='vmi.sede', verbose_name='Sede Destino'),
        ),
        migrations.CreateModel(
            name='SaldoActual',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_crea', models.DateTimeField(auto_now_add=True)),
                ('fecha_modifica', models.DateTimeField(auto_now=True)),
                ('cantidad', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('observacion', models.CharField(default='C', max_length=100, verbose_name='Observaciones')),
                ('temp_almacenamiento', models.CharField(default='22', max_length=5, verbose_name='Temperatura de almacenamiento')),
                ('bodega', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vmi.bodega')),
                ('referencia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vmi.referencia')),
            ],
            options={
                'verbose_name': 'Saldo Actual',
                'verbose_name_plural': 'Saldos Actuales',
            },
        ),
        migrations.AddField(
            model_name='referencia',
            name='tipo_unida',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='vmi.unidadtipo'),
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_proveedor', models.CharField(max_length=200)),
                ('nit', models.CharField(max_length=15, unique=True)),
                ('numero_tel_1', models.CharField(max_length=7)),
                ('numero_tel_cel', models.CharField(max_length=10)),
                ('correo', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('estado_proveedor', models.CharField(choices=[('A', 'Activo'), ('I', 'Inhabilitado'), ('C', 'Cancelado')], default='A', max_length=1)),
                ('ciudad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vmi.ciudad')),
            ],
            options={
                'verbose_name_plural': 'Proveedores',
            },
        ),
        migrations.CreateModel(
            name='PedidoRefPB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(verbose_name='Cantidad Solicitada')),
                ('concepto', models.CharField(max_length=100, verbose_name='Concepto de Referencia')),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vmi.pedidopb')),
                ('referencia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vmi.referencia')),
            ],
            options={
                'verbose_name': 'Referencia de Pedido',
                'verbose_name_plural': 'Referencias de Pedidos',
            },
        ),
        migrations.CreateModel(
            name='PedidoRefBB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(verbose_name='Cantidad Solicitada')),
                ('concepto', models.CharField(max_length=100, verbose_name='Concepto de Referencia')),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vmi.pedidobb')),
                ('referencia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vmi.referencia')),
            ],
            options={
                'verbose_name': 'Referencia de Pedido',
                'verbose_name_plural': 'Referencias de Pedidos',
            },
        ),
        migrations.AddField(
            model_name='pedidopb',
            name='proveedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vmi.proveedor'),
        ),
        migrations.AddField(
            model_name='pedidopb',
            name='sede_solicitante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vmi.sede'),
        ),
        migrations.AddField(
            model_name='pedidobb',
            name='sede_solicitante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vmi.sede'),
        ),
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saldo_inicial', models.DecimalField(decimal_places=3, default=0, max_digits=12)),
                ('entrada_inventario', models.DecimalField(decimal_places=3, default=0, max_digits=12)),
                ('salidad_inventario', models.DecimalField(decimal_places=3, default=0, max_digits=12)),
                ('saldo_final', models.DecimalField(decimal_places=3, default=0, max_digits=12)),
                ('bodega', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vmi.bodega')),
                ('periodo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vmi.periodo')),
                ('tipo_unidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vmi.unidadtipo')),
            ],
        ),
        migrations.CreateModel(
            name='IngresoRefPB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empaque', models.CharField(choices=[('C', 'Cumple'), ('NC', 'No Cumple')], max_length=2, verbose_name='Empaque/Embalaje en General')),
                ('lote', models.CharField(max_length=8, verbose_name='Lote de paquete')),
                ('fecha_vencimiento', models.DateField(verbose_name='Fecha de Vencimiento')),
                ('cantidad', models.IntegerField(verbose_name='Cantidad Referencia Recibida')),
                ('observaciones', models.CharField(max_length=200, verbose_name='Observaciones')),
                ('integridad', models.CharField(choices=[('C', 'Cumple'), ('NC', 'No Cumple')], max_length=2, verbose_name='Integridad de la Referencia')),
                ('apariencia', models.CharField(choices=[('C', 'Cumple'), ('NC', 'No Cumple')], max_length=2, verbose_name='Apariencia de la Referencia')),
                ('temp', models.CharField(max_length=2, verbose_name='Temperatura de Almacenamiento')),
                ('ingreso', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='vmi.ingresop_b', verbose_name='Ingreso Proveedor - Bodega')),
                ('referencia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vmi.referencia')),
                ('tipo_unidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vmi.unidadtipo')),
            ],
            options={
                'verbose_name': 'Referencia de Ingreso',
                'verbose_name_plural': 'Referencias de Ingresos',
            },
        ),
        migrations.CreateModel(
            name='IngresoRefBB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empaque', models.CharField(choices=[('C', 'Cumple'), ('NC', 'No Cumple')], max_length=2, verbose_name='Empaque/Embalaje en General')),
                ('lote', models.CharField(max_length=8, verbose_name='Lote de paquete')),
                ('fecha_vencimiento', models.DateField(verbose_name='Fecha de Vencimiento')),
                ('cantidad', models.IntegerField(verbose_name='Cantidad Referencia Recibida')),
                ('observaciones', models.CharField(max_length=200, verbose_name='Observaciones')),
                ('integridad', models.CharField(choices=[('C', 'Cumple'), ('NC', 'No Cumple')], max_length=2, verbose_name='Integridad de la Referencia')),
                ('apariencia', models.CharField(choices=[('C', 'Cumple'), ('NC', 'No Cumple')], max_length=2, verbose_name='Apariencia de la Referencia')),
                ('temp', models.CharField(max_length=2, verbose_name='Temperatura de Almacenamiento')),
                ('ingreso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vmi.ingresob_b', verbose_name='Ingreso Bodega - Bodega')),
                ('referencia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vmi.referencia')),
                ('tipo_unidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vmi.unidadtipo')),
            ],
            options={
                'verbose_name': 'Referencia Ingreso Bodega - Bodega',
                'verbose_name_plural': 'Referencias Ingresos Bodegas - Bodegas',
            },
        ),
        migrations.AddField(
            model_name='ingresop_b',
            name='pedido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vmi.pedidopb'),
        ),
        migrations.AddField(
            model_name='ingresop_b',
            name='proveedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='vmi.proveedor', verbose_name='Proveedor'),
        ),
        migrations.AddField(
            model_name='ingresop_b',
            name='sede_ing',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='vmi.sede', verbose_name='Sede Destino'),
        ),
        migrations.AddField(
            model_name='ingresob_b',
            name='pedido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='vmi.pedidobb'),
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
                'verbose_name': 'Factura Encabezado',
                'verbose_name_plural': 'Facturas Encabezados',
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
                'verbose_name': 'Factura Detalle',
                'verbose_name_plural': 'Facturas Detalles',
            },
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_departamento', models.CharField(max_length=200, unique=True)),
                ('codigo_dane_departamento', models.CharField(max_length=2, unique=True)),
                ('pais', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Pais', to='vmi.pais')),
            ],
        ),
        migrations.AddField(
            model_name='ciudad',
            name='departamento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Departamento', to='vmi.departamento'),
        ),
        migrations.AddField(
            model_name='bodega',
            name='municipio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vmi.ciudad'),
        ),
        migrations.AddField(
            model_name='bodega',
            name='sede',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vmi.sede'),
        ),
    ]
