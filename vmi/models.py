import datetime, uuid
from http.client import EXPECTATION_FAILED
from email.policy import default
from django.db import models
from django.utils import timezone

# Create your models here.
# ======================== Modelos de Región ========================
# ====== Model Pais ========================
class Pais(models.Model):
    nombre_pais = models.CharField(max_length=200, blank=False, null=False)
    codigo_pais = models.CharField(max_length=20, blank=False, null=False)

    def __str__(self):
        return self.nombre_pais


# ====== Model Departamento ========================
class Departamento(models.Model):
    pais = models.ForeignKey(to=Pais, on_delete=models.CASCADE, related_name='Pais')
    nombre_departamento = models.CharField(max_length=200,blank=False ,null=False)
    codigo_dane_departamento = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return self.nombre_departamento


# ====== Model Ciudad/Municipio ========================
class Ciudad(models.Model):
    departamento = models.ForeignKey(to=Departamento, on_delete=models.CASCADE, related_name='Departamento')
    nombre_ciudad = models.CharField(max_length=200, blank=False, null=False)
    codigo_dane_ciudad = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return self.nombre_ciudad


# ======================== Modelos de Sede Bodega ========================
# ====== Modelo Sede ========================
class Sede(models.Model):
    ESTADO = [
        ('A', 'Activo'),
        ('F', 'Fuera de Servicio'),
        ('T', 'Traslado')
    ]
    nombre_sede = models.CharField(max_length=50, verbose_name='Nombre de Sede')
    estado_sede = models.CharField(verbose_name='Estado de la Sede', max_length=1, choices=ESTADO)
    municipio = models.ForeignKey(to=Ciudad, on_delete=models.CASCADE)


# ====== Modelo Bodega ========================
class Bodega(models.Model):
    ESTADO = [
        ('Activo', 'Activo'),
        ('Inhabilitado', 'Inhabilitado'),
        ('Atrasado', 'Atrasado')
    ]
    nombre = models.CharField(verbose_name='Nombre de Bodega', max_length=50)
    estado = models.CharField(verbose_name='Esatdo de la Bodega', max_length=20, choices=ESTADO)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE)
    municipio = models.ForeignKey(to=Ciudad, on_delete=models.CASCADE)


# ======================== Modelos Tipo ========================
# ====== Tipo de Unidad ========================
class UnidadTipo(models.Model):
    tipo_unidad = models.CharField(max_length=50, primary_key=True)
    estado_unidad = models.CharField(max_length=1)
#    unidad_maestra = models.
    formula = models.DecimalField(decimal_places=6, max_digits=12)

    def __str__(self):
        return self.tipo_unidad


#====== Tipo de Movimiento ========================
class MovimientoTipo(models.Model):
    nombre_mov = models.CharField(max_length=20, primary_key=True)
#    estado = models.CharField()

    def __str__(self):
        return self.nombre_mov

    # def tipo_de_estado(self):
    #     if self.estado == True:
    #         return('Entrada')
    #     else:
    #         return('Salida')


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

    def cierre_de_estado(self):
        fecha_cierre = timezone.now() >= self.fecha_fin>= timezone.now() - datetime.timedelta(days=7)
        if fecha_cierre:
            cambio = self.estado = False
            return cambio

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
    codigo_ean8 = models.CharField(max_length=8, null=False)
    codigo_ean13 = models.CharField(max_length=13)
    codigo_ean128 = models.CharField(max_length=50)
    tipo_unida = models.ForeignKey(to=UnidadTipo, on_delete=models.PROTECT)

    def __str__(self):
        return self.nombre_ref


# ======================== Modelo de Proveedor ========================
# ====== Proveedor ========================
class Proveedor(models.Model):
    STATUS_CODE = [
        ('A', 'Activo'),
        ('I', 'Inhabilitado'),
        ('C', 'Cancelado')
    ]
    nombre_proveedor = models.CharField(max_length=200, blank=False, null=False)
    nit = models.CharField(max_length=15)
    numero_tel_1= models.CharField(max_length=7)
    numero_tel_cel = models.CharField(max_length=10)
    correo = models.EmailField(verbose_name='Email', unique=True)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)
    estado_proveedor = models.CharField(max_length=1, choices=STATUS_CODE)

    def __str__(self):
        return self.nombre_proveedor


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
    estado_orden = models.CharField(max_length=1, choices=STATUS_CODE)
    referencia_id = models.ForeignKey(to=Referencia, on_delete=models.CASCADE)
    tipo_unidad = models.ForeignKey(to=UnidadTipo, on_delete=models.CASCADE)


# ====== Modelo Pedido Movimiento ========================
class MovimientoPedido(Pedido):
    cantidad_compra = models.DecimalField(decimal_places=3, max_digits=6, default=0)
    valor_pedido = models.DecimalField(decimal_places=2, max_digits=12, default=0)


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
class MovimientoFactura(Factura):
    referencia_id = models.ManyToManyField(Referencia)
    cantidad_compra = models.DecimalField(max_digits=12, decimal_places=3)
    unidad_compra = models.ForeignKey(to=UnidadTipo, on_delete=models.CASCADE)


# ======================== Modelos de Inventario ========================
# ====== Modelo Inventario Base ========================
class Inventario(models.Model):
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE)
    saldo_inicial = models.DecimalField(decimal_places=3, max_digits=12)
    entrada_inventario = models.DecimalField(decimal_places=3, max_digits=12)
    salidad_inventario = models.DecimalField(decimal_places=3, max_digits=12)
    saldo_final = models.DecimalField(decimal_places=3, max_digits=12)
    tipo_unidad = models.ForeignKey(to=UnidadTipo, on_delete=models.CASCADE)

    def __str__(self):
        txt = '{0}'
        return txt.format()


# ====== Modelo Invetario Movimiento ========================
