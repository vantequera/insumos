# Sys
import uuid

# Django Models
from django.db import models
from django.utils import timezone

# Django Signals
from django.core.exceptions import ValidationError, ObjectDoesNotExist, EmptyResultSet
from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver
from django.db.models import Sum, Q, F, Min

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
    nombre_departamento = models.CharField(max_length=200, unique=True)
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
    nombre_ciudad = models.CharField(max_length=200, unique=True)
    codigo_dane_ciudad = models.CharField(max_length=3)

    def __str__(self):
        return self.nombre_ciudad.title()

    def departamentos(self):
        dep_nom = self.departamento.nombre_departamento
        pais_nom = self.departamento.pais.nombre_pais
        text = f'{dep_nom.title()} - {pais_nom.title()}'
        return text

    def codigo_dane(self):
        dep_cod = self.departamento.codigo_dane_departamento
        text = f'{dep_cod}{self.codigo_dane_ciudad}'
        return text

    def save(self):
        self.nombre_ciudad = self.nombre_ciudad.upper()
        super(Ciudad, self).save()

    class Meta:
        verbose_name = 'Ciudad'
        verbose_name_plural = 'Ciudades'
        ordering = ['nombre_ciudad']


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
        txt = f'{self.nombre} - {self.municipio}'
        return txt.title()

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

STATUS_ENV = [
    ('C', 'Cumple'),
    ('NC', 'No Cumple')
]
# ====== Modelo Abstracto Base ========================
class CommonInfo(models.Model):
    fecha = models.DateTimeField('Fecha y Hora')
    transporte = models.CharField('Transportadora', max_length=100)
    bodega_des = models.ForeignKey(Bodega, on_delete=models.PROTECT, verbose_name='Bodega De Ingreso')

    class Meta:
        abstract = True


class CommonInfoRef(models.Model):
    referencia = models.ForeignKey(Referencia, on_delete=models.CASCADE)
    empaque = models.CharField(verbose_name='Empaque/Embalaje en General', max_length=2, choices=STATUS_ENV)
    lote = models.CharField(verbose_name='Lote de paquete', max_length=8)
    fecha_vencimiento = models.DateField(verbose_name='Fecha de Vencimiento')
    cantidad = models.IntegerField('Cantidad Referencia Recibida')
    tipo_unidad = models.ForeignKey(UnidadTipo, on_delete=models.CASCADE)
    observaciones = models.CharField('Observaciones', max_length=200)
    integridad = models.CharField('Integridad de la Referencia', max_length=2, choices=STATUS_ENV)
    apariencia = models.CharField('Apariencia de la Referencia', max_length=2, choices=STATUS_ENV)
    temp = models.CharField('Temperatura de Almacenamiento', max_length=2)

    class Meta:
        abstract = True


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
        ('SE', 'Solicitud Enviada'),
        ('AP', 'Aprobado'),
        ('CA', 'Cancelado'),
        ('RZ', 'Rechazado'),
        ('EN', 'Enviado'),
        ('RC', 'Recibido')
    ]
    sede_solicitante = models.ForeignKey(Sede, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True, editable=False)
    estado_solicitud = models.CharField(max_length=2, choices=STATUS_CODE, default='SE')
    concepto_general = models.CharField(max_length=255, verbose_name='Concepto de solicitud')
    bodega_solicitada = models.ForeignKey(Bodega, on_delete=models.CASCADE)

    def __str__(self):
        return


# ====== Modelo Pedido Movimiento ========================
class PedidoRef(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    referencia = models.ForeignKey(Referencia, on_delete=models.CASCADE)
    cantidad = models.IntegerField(verbose_name='Cantidad Solicitada')
    concepto = models.CharField(verbose_name='Concepto de Referencia', max_length=100)


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


# ====== Modelo Inventario Movimiento ========================


# ======================== Modelos de Ingreso de Insumos ========================
# ====== Modelo de ingreso de insumos HEAD P - B ========================
class IngresoP_B(CommonInfo):
    sede_ing = models.ForeignKey(Sede, on_delete=models.PROTECT)
    factura_prov = models.CharField('Factura Recibida', max_length=50)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, verbose_name='Proveedor', null=True)

    def __str__(self):
        txt = f'{self.proveedor} ▶️ {self.bodega_des} 🟢'
        return txt

    class Meta:
        verbose_name = 'Ingreso Proveedor - Bodega'
        verbose_name_plural = 'Ingresos Proveedores - Bodegas'


# ====== Modelo de ingreso de insumos BODY P - B ========================
class IngresoRefPB(CommonInfoRef):
    ingreso = models.ForeignKey(IngresoP_B, on_delete=models.CASCADE, verbose_name='Factura de Ingreso')

    def __str__(self):
        return str(self.referencia_id)

    class Meta:
        verbose_name = 'Referencia de Ingreso'
        verbose_name_plural = 'Referencias de Ingresos'


# ====== Modelo de ingreso de insumos HEAD B-B ========================
class IngresoB_B(CommonInfo):
    pedido = models.ForeignKey(Pedido, on_delete=models.PROTECT)

    def __str__(self):
        txt = f'{self.pedido.bodega_solicitada} ▶️ {self.bodega_des} 🟢'
        return txt

    class Meta:
        verbose_name = 'Ingreso Bodega - Bodega'
        verbose_name_plural = 'Ingresos Bodegas - Bodegas'


class IngresoRefBB(CommonInfoRef):
    ingreso = models.ForeignKey(IngresoB_B, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.referencia_id)

    class Meta:
        verbose_name = 'Referencia Ingreso Bodega - Bodega'
        verbose_name_plural = 'Referencias Ingresos Bodegas - Bodegas'


# ======================== Modelos de Salida de Insumos ========================
# ====== Modelo de Salida de insumos HEAD ========================
class Salida(CommonInfo):
    sede_des = models.ForeignKey(Sede, on_delete=models.PROTECT, verbose_name='Sede Destino', default=1)

    def __str__(self):
        txt = f'Salida {self.bodega_des} 🔴'
        return txt

    class Meta:
        verbose_name = 'Salida de Referencia'
        verbose_name_plural = 'Salidas de Referencias'


# ====== Modelo de Salida de insumos BODY ========================
class SalidaRef(CommonInfoRef):
    salida = models.ForeignKey(Salida, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.referencia_id)

    class Meta:
        verbose_name = 'Referencia de Salida'
        verbose_name_plural = 'Referencias de Salidas'


# ======================== Modelo de Saldos ========================
# ====== Saldo Actual ========================
class SaldoActual(Modelo):
    referencia = models.ForeignKey(Referencia, on_delete=models.CASCADE)
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE)
    cantidad = models.DecimalField(decimal_places=2, max_digits=6, default=0)
    observacion = models.CharField(verbose_name='Observaciones', max_length=100, default='C')
    temp_almacenamiento = models.CharField(verbose_name='Temperatura de almacenamiento', max_length=5, default='22')

    def __str__(self):
        txt = '{0}'.format(self.referencia)
        return txt

    def temp_alm(self):
        text = f'{self.temp_almacenamiento} °C'
        return text

    class Meta:
        verbose_name = 'Saldo Actual'
        verbose_name_plural = 'Saldos Actuales'



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


# ====== Signals de Referencias creadas ========================
@receiver(post_save, sender=Referencia)
def ingreso_referencia(sender, instance, **kwargs):
    ref_id = instance.id
    try:
        if SaldoActual.objects.get(referencia__pk=ref_id):
            print('Referencia en existencia')

    except ObjectDoesNotExist:
        ref = Referencia.objects.get(pk=ref_id)
        bodegas = Bodega.objects.all()
        for bodega in bodegas:
            saldo = SaldoActual(
                referencia=ref,
                bodega=bodega
            )
            saldo.save()


# ======= Signal de ingreso de insumos ========================
@receiver(post_save, sender=IngresoRefPB)
def ingreso_insumo(sender, instance, **kwargs):
    bod_des = instance.ingreso.bodega_des.id
    referencia_id = instance.referencia.id
    saldo = SaldoActual.objects.get(Q(bodega__pk=bod_des) & Q(referencia__pk=referencia_id))
    if saldo:
        saldo.cantidad = saldo.cantidad + instance.cantidad
        saldo.observacion = instance.observaciones
        saldo.temp_almacenamiento = instance.temp
        saldo.save()


# ======= Signal de salida de insumos ========================
@receiver(post_save, sender=SalidaRef)
def salida_insumo(sender, instance, **kwargs):
    bod_des = instance.salida.bodega_des.id
    referencia_id = instance.referencia.id
    saldo_sal = SaldoActual.objects.get(Q(bodega__pk=bod_des) & Q(referencia__pk=referencia_id))
    if saldo_sal:
        saldo_sal.cantidad = saldo_sal.cantidad - instance.cantidad
        saldo_sal.save()


# ====== Signal de Bodega ligado a referencias de insumos ========================
@receiver(post_save, sender=Bodega)
def creacion_saldos(sender, instance, **kwargs):
    bodega_id = instance.id
    try:
        saldos = SaldoActual.objects.filter(bodega__pk=bodega_id)
        saldo_list = list(saldos)
        if len(saldo_list) == 0:
            print('Bodega sin los Saldos Actuales')
            raise EmptyResultSet

    except EmptyResultSet:
        bod_nueva = Bodega.objects.get(pk=bodega_id)
        referencias = Referencia.objects.all()
        for ref in referencias:
            saldo = SaldoActual(
                referencia=ref,
                bodega=bod_nueva
            )
            saldo.save()


# ===== Signals del área de facturación ========================
@receiver(post_save, sender=FacturaDet)
def detalle_fac_guardar(sender, instance, **kwargs):
    """Signal para el descuento de items en los detalles de facturas"""
    factura_id = instance.factura.id
    referencia_id = instance.producto.id
    factura_encabezado = FacturaEnc.objects.get(pk=factura_id)

    """ Suma de callbacks de valores hacia Factura Encabezado """
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
    producto_a_cambiar = SaldoActual.objects.get(referencia__pk=referencia_id)
    producto_cantidad = int(producto_a_cambiar.cantidad)
    instancia_cantidad = int(instance.cantidad)
    producto_temperatura = producto_a_cambiar.temp_almacenamiento

    """ Comprobación de instancias para descontar """
    if instancia_cantidad > producto_cantidad:
        nueva_cant = producto_cantidad - instancia_cantidad
        producto_cantidad = nueva_cant
        producto_a_cambiar.temp_almacenamiento = producto_temperatura
        producto_a_cambiar.save()

    else:
        raise ValidationError