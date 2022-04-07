import datetime
from django.db import models
from django.forms import DateTimeField
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


# ======================== Modelo Tipo de Unidad ========================
# ====== Tipo de Unidad ========================
class TypeUnit(models.Model):
    tipo_unidad = models.CharField(max_length=50, primary_key=True)
    estado_unidad = models.CharField(max_length=1)

    def __str__(self):
        return self.tipo_unidad


# ======================== Modelo de Referencia ========================
# ====== Referencia de productos ========================
class Reference(models.Model):
    nombre_ref = models.CharField(max_length=100)
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
    pass


# ====== Modelo Pedido Movimiento ========================
class MovementOrder(Order):
    pass


# ====== Modelo Pedido Proveedores ========================
class ProviderOrder(Order):
    pass


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