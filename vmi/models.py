import datetime, uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
# from django_userforeignkey.models.fields import UserForeignKey

# Django Signals
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db.models import Sum

# Create your models here.
# ======================== Modelo de usuarios ========================
# ====== Usuario Modelo Abstracto ========================
class Modelo(models.Model):
    fecha_crea = models.DateTimeField(auto_now_add=True)
    fecha_modifica = models.DateTimeField(auto_now=True)
    # usuario_crea = UserForeignKey(auto_user_add=True, related_name='+') # <== Anula el mapeo en reversa con el '+'
    # usuario_modifica = UserForeignKey(auto_user=True, related_name='+')

    class Meta:
        abstract = True


# ====== Usuario Modelo Principal ========================
class Usuario():
    pass


# ======================== Modelos de Región ========================
# ====== Model Pais ========================
class Pais(models.Model):
    nombre_pais = models.CharField(max_length=200, blank=False, null=False)
    codigo_pais = models.CharField(max_length=20, blank=False, null=False, unique=True)

    def __str__(self):
        return self.nombre_pais.title()

    def save(self):
        self.nombre_pais = self.nombre_pais.upper()
        super(Pais, self).save()

    class Meta:
        verbose_name_plural = 'Paises'


# ====== Model Departamento ========================
class Departamento(models.Model):
    pais = models.ForeignKey(to=Pais, on_delete=models.CASCADE, related_name='Pais')
    nombre_departamento = models.CharField(max_length=200,blank=False ,null=False)
    codigo_dane_departamento = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return self.nombre_departamento.title()

    def save(self):
        self.nombre_departamento = self.nombre_departamento.upper()
        super(Departamento, self).save()

    # class Meta:
    #     verbose_name_plural = 'Departamentos'


# ====== Model Ciudad/Municipio ========================
class Ciudad(models.Model):
    departamento = models.ForeignKey(to=Departamento, on_delete=models.CASCADE, related_name='Departamento')
    nombre_ciudad = models.CharField(max_length=200, blank=False, null=False)
    codigo_dane_ciudad = models.CharField(max_length=3)

    def __str__(self):
        return self.nombre_ciudad.title()

    def save(self):
        self.nombre_ciudad = self.nombre_ciudad.upper()
        super(Ciudad, self).save()

    class Meta:
        verbose_name_plural = 'Ciudades'


# ======================== Modelos de Sede Bodega ========================
# ====== Modelo Sede ========================
class Sede(models.Model):
    ESTADO = [
        ('O', 'Operativo'),
        ('F', 'Fuera de Servicio'),
        ('T', 'Traslado')
    ]
    nombre_sede = models.CharField(max_length=50, verbose_name='Nombre de Sede')
    estado_sede = models.CharField(verbose_name='Estado de Sede', max_length=1, choices=ESTADO, default='O')
    municipio = models.ForeignKey(to=Ciudad, on_delete=models.CASCADE)
    direccion = models.CharField(verbose_name='Dirección', max_length=50, default='none')

    def __str__(self):
        text = f'{self.nombre_sede} - {self.municipio}'
        return text

    def save(self):
        self.nombre_sede = self.nombre_sede.upper()
        super(Sede, self).save()


# ====== Modelo Bodega ========================
class Bodega(models.Model):
    ESTADO = [
        ('Activo', 'Activo'),
        ('Inhabilitado', 'Inhabilitado'),
        ('Atrasado', 'Atrasado')
    ]
    nombre = models.CharField(verbose_name='Nombre de Bodega', max_length=50)
    estado = models.CharField(verbose_name='Estado de la Bodega', max_length=20, choices=ESTADO, default='A')
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE)
    municipio = models.ForeignKey(Ciudad, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre.title()

    def save(self):
        self.nombre = self.nombre.upper()
        super(Bodega, self).save()

# ======================== Modelos Tipo ========================
# ====== Tipo de Unidad ========================
class UnidadTipo(models.Model):
    ESTADO = [
        ('A', 'Activo'),
        ('I', 'Inactivo')
    ]
    tipo_unidad = models.CharField(max_length=50, primary_key=True)
    estado_unidad = models.CharField(max_length=1, choices=ESTADO)
#    unidad_maestra = models.CharField(max_length=50)
    formula = models.DecimalField(decimal_places=6, max_digits=12)

    def save(self):
        self.tipo_unidad = self.tipo_unidad.upper()
        super(UnidadTipo, self).save()

    def __str__(self):
        return self.tipo_unidad.title()


#====== Tipo de Movimiento ========================
class MovimientoTipo(models.Model):
    IN = 'Entrada_Bodega'
    OUT = 'Salida_Bodega'
    MOVES = [
        (IN, 'Entrada de Bodega'),
        (OUT, 'Salida de Bodega')
    ]
    nombre_mov = models.CharField(max_length=30, primary_key=True)
    estado = models.CharField(max_length=14, choices=MOVES, default=IN)

    def save(self):
        self.nombre_mov = self.nombre_mov.upper()
        super(MovimientoTipo, self).save()

    def __str__(self):
        return self.nombre_mov.title()

    def tipo_de_estado(self):
        if self.estado == 'Entrada_Bodega':
            return('🟢')
        else:
            return('🔴')


# ====== Modelo de periodos de facturación ========================
class Periodo(models.Model):
    fecha_inicio = models.DateField("Inicio del corte")
    fecha_fin = models.DateField("Fin del corte")
    estado = models.BooleanField(default=True, verbose_name='Estado del periodo')

    def __str__(self):
        inicio = self.fecha_inicio.strftime('%d/%B/%Y')
        fin = self.fecha_fin.strftime('%d/%B/%Y')
        txt = '{0} - {1}'.format(inicio, fin)
        return txt

    # def cierre_de_estado(self):
    #     fecha_cierre = timezone.now() >= self.fecha_fin>= timezone.now() - datetime.timedelta(days=7)
    #     if fecha_cierre:
    #         cambio = self.estado = False
    #         return cambio

    def estado_del_periodo(self):
        if self.estado == True:
            return 'Activo'
        else:
            return 'Cerrado'


# ======================== Modelo de Referencia ========================
# ====== Referencia de productos ========================
class Referencia(models.Model):
    nombre_ref = models.CharField(max_length=100)
    unique_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    codigo_ean8 = models.CharField(max_length=8, unique=True)
    codigo_ean13 = models.CharField(max_length=13, unique=True)
    codigo_ean128 = models.CharField(max_length=50)
    tipo_unida = models.ForeignKey(to=UnidadTipo, on_delete=models.PROTECT)

    def __str__(self):
        return self.nombre_ref.title()

    def save(self):
        self.nombre_ref = self.nombre_ref.upper()
        super(Referencia, self).save()


# ======================== Modelo de Proveedor ========================
# ====== Proveedor ========================
class Proveedor(models.Model):
    STATUS_CODE = [
        ('A', 'Activo'),
        ('I', 'Inhabilitado'),
        ('C', 'Cancelado')
    ]
    nombre_proveedor = models.CharField(max_length=200, blank=False, null=False)
    nit = models.CharField(max_length=15, unique=True)
    numero_tel_1= models.CharField(max_length=7)
    numero_tel_cel = models.CharField(max_length=10)
    correo = models.EmailField(verbose_name='Email', unique=True)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)
    estado_proveedor = models.CharField(max_length=1, choices=STATUS_CODE)

    def __str__(self):
        return self.nombre_proveedor

    def save(self):
        self.nombre_proveedor = self.nombre_proveedor.title()
        super(Proveedor, self).save()

    class Meta:
        verbose_name_plural = 'Proveedores'


# ======================== Modelos de Pedidos ========================
# ====== Modelo Pedido General ========================
class Pedido(models.Model):
    STATUS_CODE = [
        ('A', 'Activo'),
        ('E', 'En Curso'),
        ('C', 'Cancelado'),
        ('P', 'Pago')
    ]
    proveedor_id = models.ForeignKey(to=Proveedor, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True, editable=False)
    estado_orden = models.CharField(max_length=1, choices=STATUS_CODE, default='A')
    valor_pedido = models.ForeignKey('MovimientoPedido', models.DO_NOTHING, db_column='valor_pedido', default=0, related_name='+')

    # def save(self):
    #     movimiento = Pedido.objects.all().get(id=self.id)
    #     movimiento.valor_pedido.valor_movimiento = F('valor_movimiento')
    #     self.valor_pedido = movimiento.valor_pedido.valor_movimiento
    #     super(Pedido, self).save()


# ====== Modelo Pedido Movimiento ========================
class MovimientoPedido(Pedido):
    referencia_id = models.ManyToManyField(Referencia)
    cantidad_solicitada = models.DecimalField(decimal_places=3, max_digits=6, default=0)
    tipo_unidad = models.ForeignKey(to=UnidadTipo, on_delete=models.CASCADE, default='A')
    valor_movimiento = models.DecimalField(decimal_places=2, max_digits=12, default=0)

# ====== Calculo de valor total ==========================
    def _get_valor_compra(self):
        return self.cantidad_solicitada*self.valor_movimiento

    valor_compra = property(_get_valor_compra) # <== Ya no es necesario


# ====== Modelo Pedido Proveedores ========================
class ProveedorPedido(Pedido):
    cantidad_compra = models.DecimalField(decimal_places=3, max_digits=6, default=0)
    valor_orden = models.DecimalField(decimal_places=3, max_digits=6, default=0)


# ======================== Modelos de Facturación ========================
# ====== Modelo Factura General ========================
class Factura(models.Model):
    proveedor_id = models.ForeignKey(to=Proveedor, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True, editable=False,)
    fecha_facturacion = models.DateTimeField()
    concepto = models.CharField(max_length=100)

    def __str__(self):
        return self.concepto


# ====== Modelo Factura de Movimiento ========================
# class MovimientoFactura(Factura):
#     referencia_id = models.ManyToManyField(Referencia)
#     cantidad_compra = models.DecimalField(max_digits=12, decimal_places=3)
#     unidad_compra = models.ForeignKey(to=UnidadTipo, on_delete=models.CASCADE)


# ======================== Modelos de Inventario ========================
# ====== Modelo Inventario Base ========================
class Inventario(models.Model):
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE)
    saldo_inicial = models.DecimalField(decimal_places=3, max_digits=12, default=0)
    entrada_inventario = models.DecimalField(decimal_places=3, max_digits=12, default=0)
    salidad_inventario = models.DecimalField(decimal_places=3, max_digits=12, default=0)
    saldo_final = models.DecimalField(decimal_places=3, max_digits=12, default=0)
    tipo_unidad = models.ForeignKey(to=UnidadTipo, on_delete=models.CASCADE)

    def save(self):
        entrada = float(float(self.saldo_inicial) + float(self.entrada_inventario))
        self.saldo_final = entrada - float(self.salidad_inventario)
        if self.periodo.estado != True:
            raise ValidationError(message='El operiodo de facturación cerró')
        else:
            super(Inventario, self).save()

    def __str__(self):
        txt = '{0}'
        return txt.format(self.bodega)


# ====== Modelo Invetario Movimiento ========================


# ======================== Modelo de Saldos ========================
# ====== Saldo Actual ========================
class SaldoActual(Modelo):
    referencia = models.ForeignKey(Referencia, on_delete=models.CASCADE)
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE)
    cantidad = models.DecimalField(decimal_places=2, max_digits=6, default=0)
    observacion = models.CharField(verbose_name='Observaciones', max_length=100, default='22')
    temp_almacenamiento = models.CharField(
        verbose_name='Temperatura de almacenamiento',
        max_length=5,
        default='22'
    )

    def __str__(self):
        txt = '{0}'.format(self.referencia)
        return txt

    def save(self):
        temp = f'{self.temp_almacenamiento} °C'
        self.temp_almacenamiento = temp
        super(SaldoActual, self).save()

    class Meta:
        verbose_name = 'Saldo Actual'
        verbose_name_plural = 'Saldos Actuales'


@receiver(post_save, sender=Referencia)
def ingreso_referencia(sender, instance, **kwargs):
    ref_id = instance.id
    ref = Referencia.objects.get(pk=ref_id)
    sald = SaldoActual.objects.get(referencia=ref)
    sal_id = sald.referencia.id
    if sal_id != ref_id:
        bog = Bodega.objects.get(pk=1)
        saldo = SaldoActual(
            referencia=ref,
            bodega=bog
        )
        saldo.save()


# ====== Saldo Histórico ========================
class SaldoHistorico(models.Model):
    pass


# ======================== Facturación ========================
# ====== Facturación Encabezado ========================
class FacturaEnc(Modelo):
    """
        Modelo de Factura Encabezado: *Mas parecido al modelo de traslado*
        Modelo para generar facturas en el área de insumos con
        sus respectivos campos de: *Proveedor al cual se le debe,
        fecha a la cual pertenece la factura,
        subtotal de todos los precios en la parte del cuerpo de la factura,
        descuento total recibido en los productos adquiridos,
        total a pagar en la factura que se generó
    """
    cliente = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    sub_total = models.FloatField(default=0)
    descuento = models.FloatField(default=0)
    total = models.FloatField(default=0)

    def __str__(self):
        return '{0}'.format(self.cliente)

    class Meta:
        verbose_name = 'Factura Encabezado'
        verbose_name_plural = 'Facturas Encabezados'
        # permissions = [
        #     ('sup_caja_fac', 'Permisos de CRUD para crear y editar facturas')
        # ]


# ====== Facturación Detalles ========================
class FacturaDet(Modelo):
    """
        Modelo de Factura Detalle:
        Modelo para generar el cuerpo de las facturas con
        sus respectivos campos de: Factura Encabezado a la cual pertenece,
        producto al cual se está haciendo la salida,
        cantidad por unidades basado en su estado,
        precio equivalente por unidad,
        sub total equivalente a la multiplicación de la cantidad con el precio,
        descuento total recibido por itém,
        total en precio pesos colombianos
    """
    factura = models.ForeignKey(FacturaEnc, on_delete=models.CASCADE)
    producto = models.ForeignKey(Referencia, on_delete=models.CASCADE)
    cantidad = models.BigIntegerField(default=0)
    precio = models.FloatField(default=0)
    sub_total = models.FloatField(default=0)
    descuento = models.FloatField(default=0)
    total = models.FloatField(default=0)

    def __str__(self):
        return '{0}'.format(self.producto)

    def save(self):
        self.sub_total = float(int(self.cantidad) * float(self.precio))
        self.total = self.sub_total - float(self.descuento)
        super(FacturaDet, self).save()

    class Meta:
        verbose_name = 'Factura Detalle'
        verbose_name_plural = 'Facturas Detalles'
        # permissions = [
        #     ('sup_caja_fac', 'Permisos de CRUD para crear y editar facturas')
        # ]


# === Signals del área de facturación ========================
@receiver(post_save, sender=FacturaDet)
def detalle_fac_guardar(sender, instance, **kwargs):
    """Signal para el descuento de items en los detalles de facturas"""
    factura_id = instance.factura.id
    referencia_id = instance.producto.id

    """ Suma de callbacks de valores hacia Factura Encabezado """
    factura_encabezado = FacturaEnc.objects.get(pk=factura_id)
    if factura_encabezado:
        sub_total = FacturaDet.objects.filter(factura=factura_id).aggregate(
            sub_total=Sum('sub_total')).get('sub_total', 0.00
        )
        descuento = FacturaDet.objects.filter(factura=factura_id).aggregate(
            descuento=Sum('descuento')).get('descuento', 0.00
        )
        factura_encabezado.sub_total = sub_total
        factura_encabezado.descuento = descuento
        factura_encabezado.total = sub_total - descuento
        factura_encabezado.save()

    """ Descontar las cantidades por cada referencia """
    producto_a_cambiar = SaldoActual.objects.get(referencia=referencia_id)
    producto_cantidad = int(producto_a_cambiar.cantidad)
    instancia_cantidad = int(instance.cantidad)
    producto_temperatura = producto_a_cambiar.temp_almacenamiento
    if instancia_cantidad > producto_cantidad:
        nueva_cant = producto_cantidad - instancia_cantidad
        producto_cantidad = nueva_cant
        producto_a_cambiar.temp_almacenamiento = producto_temperatura
        producto_a_cambiar.save()