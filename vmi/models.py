from django.db import models
from django.utils import timezone

# Create your models here.

"""
Modelos con PrimaryKey
"""
class Reference (models.Model):
    idReferencia = models.PositiveSmallIntegerField(primary_key=True, null=False)
    nombre = models.CharField(max_length=50, null=False, blank=False)
    ean13 = models.CharField(max_length=50, null=False)
    ean8 = models.CharField(max_length=50, null=False)
    ean128 = models.CharField(max_length=50, null=False)


class Proveedor (models.Model):
    idProveedor = models.PositiveSmallIntegerField(primary_key=True, null=False)
    nombre = models.CharField(max_length=50, null=False)
    fecha_creacion = models.DateTimeField(timezone.now())
#    estado = models.BooleanField(default=False)


class TipoUnidad (models.Model):
    idUnidad = models.PositiveSmallIntegerField(primary_key=True, null=False)
    tipo_unidad = models.CharField(max_length=50, null=False)
#    estado = models.BooleanField(default=False)


class Sede (models.Model):
    idSede = models.PositiveSmallIntegerField(primary_key=True, null=False)
    nombre_sede = models.CharField(max_length=50, null=False)
#    estado = models.BooleanField(default=False)


"""
Modelos con PrimaryKey y ForeignKey
"""


class Bodega (models.Model):
    idBodega = models.PositiveSmallIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50, null=False)
    idSede = models.ForeignKey(Sede, null=False, on_delete=models.CASCADE)
#    estado = models.BooleanField(default=False)


class Factura (models.Model):
    idFactura = models.PositiveSmallIntegerField(primary_key=True, null=False)
    idProveedor = models.ForeignKey(
        Proveedor, null=False, blank=False, on_delete=models.CASCADE)
    fechaFactura = models.DateTimeField(timezone.now())
#    estado = models.BooleanField(default=False)


class TipoMov (models.Model):
    idTipoMov = models.AutoField(primary_key=True, null=False)
    tipo_mov = models.CharField(max_length=50, null=False)
    signo = models.PositiveSmallIntegerField(null=False)
#    estado = models.BooleanField(default=False)


class Pedido (models.Model):
    idPedido = models.AutoField(primary_key=True)
    idProveedor = models.ForeignKey(
        Proveedor, null=False, blank=False, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(timezone.now())
#    estado = models.BooleanField(default=False)

class PedidosMov (models.Model):
    idPedido = models.ForeignKey(
        Pedido, null=False, blank=False, on_delete=models.CASCADE)
    idNumero = models.PositiveSmallIntegerField(primary_key=True, null=False)
    idReferencia = models.ForeignKey(Reference, null=False, blank=False, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(timezone.now())
    cantidad = models.PositiveIntegerField(null=False, blank=False, default=0)
    idUnidadCompra = models.ForeignKey(
        TipoUnidad, null=False, blank=False, on_delete=models.CASCADE)


class Inventario (models.Model):
    idReferencia = models.ForeignKey(
        Reference, null=False, blank=False, on_delete=models.CASCADE)
    idbodega = models.ForeignKey(
        Bodega, null=False, blank=False, on_delete=models.CASCADE)
    saldo = models.PositiveIntegerField('Saldo')
#    estado = models.BooleanField(default=False)


class MovInventario (models.Model):
    idMovimiento = models.AutoField(primary_key=True)
    idReferencia = models.ForeignKey(
        Reference, null=False, blank=False, on_delete=models.CASCADE)
    idBodega = models.ForeignKey(
        Bodega, null=False, blank=False, on_delete=models.CASCADE)
    idTipoUnidadMov = models.ForeignKey(
        TipoUnidad, null=False, blank=False, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(null=False)
    idTipoMov = models.ForeignKey(
        TipoMov, null=False, blank=False, on_delete=models.CASCADE)
    fechaMov = models.DateTimeField(timezone.now())
    idFactura = models.ForeignKey(
        Factura, null=False, on_delete=models.CASCADE)


class FacturaPedido (models.Model):
    idFactura = models.ForeignKey(
        Factura, null=False, blank=False, on_delete=models.CASCADE)
    idPedido = models.ForeignKey(
        Pedido, null=False, blank=False, on_delete=models.CASCADE)


class FacturasMov (models.Model):
    idfactura = models.ForeignKey(
        Factura, null=False, blank=False, on_delete=models.CASCADE)
    idNumero = models.AutoField(primary_key=True)
    ideReferencia = models.ForeignKey(
        Reference, null=False, blank=False, on_delete=models.CASCADE)
    fechaPedido = models.DateTimeField(auto_now_add=True)