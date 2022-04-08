import datetime, uuid
from email.policy import default
from django.db import models
from django.utils import timezone

# Create your models here.
# ======================== Modelos de Región ========================
# ====== Model Pais ========================
class Country(models.Model):
    nombre_pais = models.CharField(max_length=200, blank=False, null=False)
    codigo_pais = models.CharField(max_length=20, blank=False, null=False)

    def __str__(self):
        return self.nombre_pais


# ====== Model Departamento ========================
class Department(models.Model):
    pais = models.ForeignKey(Country,on_delete=models.CASCADE ,related_name='Pais')
    nombre_departamento = models.CharField(max_length=200,blank=False ,null=False)
    codigo_dane_departamento = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return self.nombre_departamento


# ====== Model Ciudad/Municipio ========================
class City(models.Model):
    departamento = models.ForeignKey(Department,on_delete=models.CASCADE ,related_name='Departamento')
    nombre_ciudad = models.CharField(max_length=200, blank=False, null=False)
    codigo_dane_ciudad = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return self.nombre_ciudad


# ======================== Modelos Tipo ========================
# ====== Tipo de Unidad ========================
class TypeUnit(models.Model):
    tipo_unidad = models.CharField(max_length=50, primary_key=True)
    estado_unidad = models.CharField(max_length=1)
#    unidad_maestra = models.
    formula = models.DecimalField(decimal_places=6, max_digits=12)

    def __str__(self):
        return self.tipo_unidad


#====== Tipo de Movimiento ========================
class TypeMov(models.Model):
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
class Reference(models.Model):
    nombre_ref = models.CharField(max_length=100)
    unique_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    codigo_ean8 = models.CharField(max_length=8, null=False)
    codigo_ean13 = models.CharField(max_length=13)
    codigo_ean128 = models.CharField(max_length=50)
    tipo_unida = models.ForeignKey(TypeUnit, on_delete=models.PROTECT)

    def __str__(self):
        return self.nombre_ref


# ======================== Modelo de Proveedor ========================
# ====== Proveedor ========================
class Provider(models.Model):
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
    ciudad = models.ForeignKey(City, on_delete=models.CASCADE)
    estado_proveedor = models.CharField(max_length=1, choices=STATUS_CODE)

    def __str__(self):
        return self.nombre_proveedor


# ======================== Modelos de Pedidos ========================
# ====== Modelo Pedido General ========================
class Order(models.Model):
    STATUS_CODE = [
        ('A', 'Activo'),
        ('E', 'En Curso'),
        ('C', 'Cancelado'),
        ('P', 'Pago')
    ]
    proveedor_id = models.ForeignKey(Provider, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True, editable=False)
    estado_orden = models.CharField(max_length=1, choices=STATUS_CODE)
    referencia_id = models.ForeignKey(Reference, on_delete=models.CASCADE)
    tipo_unidad = models.ForeignKey(TypeUnit, models.CASCADE)


# ====== Modelo Pedido Movimiento ========================
class MovementOrder(Order):
    cantidad_compra = models.DecimalField(decimal_places=3, max_digits=6, default=0)
    valor_pedido = models.DecimalField(decimal_places=2, max_digits=12, default=0)


# ====== Modelo Pedido Proveedores ========================
class ProviderOrder(Order):
    cantidad_compra = models.DecimalField(decimal_places=3, max_digits=6, default=0)
    valor_orden = models.DecimalField(decimal_places=3, max_digits=6, default=0)


# ======================== Modelos de Facturación ========================
# ====== Modelo Factura General ========================
class Billing(models.Model):
    proveedor_id = models.ForeignKey(Provider, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True, editable=False,)
    fecha_facturacion = models.DateTimeField()
    concepto = models.CharField(max_length=100)

    def __str__(self):
        return self.concepto


# ====== Modelo Factura de Movimiento ========================
class MovementBilling(Billing):
    referencia_id = models.ManyToManyField(Reference)
    cantidad_compra = models.DecimalField(max_digits=12, decimal_places=3)
    unidad_compra = models.ForeignKey(TypeUnit, on_delete=models.CASCADE)