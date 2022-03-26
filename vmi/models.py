from django.db import models
from django.utils import timezone

# Create your models here.

"""
Modelos con PrimaryKey
"""
class Referencia (models.Model):
    idReferencia = models.BigIntegerField(primary_key=True, null=False)
    nombre = models.CharField(max_length=50, null=False, blank=False)
    ean13 = models.CharField(max_length=50, null=False)
    ean8 = models.CharField(max_length=50, null=False)
    ean128 = models.CharField(max_length=50, null=False)
    cantidad = models.IntegerField(null=False, blank=False, default=0)
    def __str__(self):
        return self.nombre
#        txt = '{0} ({1})'
#        return txt.format(self.nombre, self.idReferencia)


class Proveedor (models.Model):
    idProveedor = models.PositiveIntegerField(primary_key=True, null=False)
    nombre = models.CharField(max_length=50, null=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True, editable=False,)
    def __str__(self):
        return self.nombre
#        txt = '{0} Fecha ({1})'
#        return txt.format(self.nombre, self.fecha_creacion.strftime('%b/%d/%Y - %H:%M'))
#    estado = models.BooleanField(default=False)


class TipoUnidad (models.Model):
    idUnidad = models.PositiveIntegerField(primary_key=True, null=False)
    tipo_unidad = models.CharField(max_length=50, null=False)
    def __str__(self):
        return self.tipo_unidad
#    estado = models.BooleanField(default=False)


class Sede (models.Model):
    idSede = models.PositiveIntegerField(primary_key=True, null=False)
    nombre_sede = models.CharField(max_length=50, null=False)
    def __str__(self):
        return self.nombre_sede
        # txt = '{0} (ID {1})'
        # return txt.format(self.nombre_sede, self.idSede)
#    estado = models.BooleanField(default=False)


"""
Modelos con PrimaryKey y ForeignKey
"""


class Bodega (models.Model):
    idBodega = models.PositiveIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50, null=False)
    idSede = models.ForeignKey(Sede, null=False, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre
#    estado = models.BooleanField(default=False)


class Factura (models.Model):
    idFactura = models.PositiveIntegerField(primary_key=True, null=False)
    idProveedor = models.ForeignKey(Proveedor, null=False, blank=False, on_delete=models.CASCADE)
    fechaFactura = models.DateTimeField(auto_now_add=True, editable=False)
    def __str__(self):
        return str(self.idProveedor)
        # txt = '{0} - {1}'.format(self.idProveedor, self.fechaFactura.strftime('%b/%d/%Y'))
        # return txt
#    estado = models.BooleanField(default=False)


class TipoMov (models.Model):
    idTipoMov = models.AutoField(primary_key=True, null=False)
    tipo_mov = models.CharField(max_length=50, null=False)
    signo = models.PositiveSmallIntegerField(null=False)
    # estado = models.BooleanField(default=False)
    def __str__(self):
        return self.tipo_mov


class Pedido (models.Model):
    idPedido = models.AutoField(primary_key=True)
    idProveedor = models.ForeignKey(Proveedor, null=False, blank=False, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True, editable=False)
    def __str__(self):
        return str(self.idProveedor)
#    estado = models.BooleanField(default=False)

class PedidosMov (models.Model):
    idPedido = models.ForeignKey(Pedido, null=False, blank=False, on_delete=models.CASCADE)
    idNumero = models.PositiveIntegerField(primary_key=True, null=False)
    idReferencia = models.ForeignKey(Referencia, null=False, blank=False, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True, editable=False)
    cantidad = models.PositiveIntegerField(null=False, blank=False, default=0, editable=False)
    idUnidadCompra = models.ForeignKey(TipoUnidad, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        txt = '{0} Ref ({1}, {2})'
        return str(txt.format(self.idPedido, self.idReferencia, self.cantidad))


class Inventario (models.Model):
    idReferencia = models.ForeignKey(Referencia, null=False, blank=False, on_delete=models.CASCADE)
    idbodega = models.ForeignKey(Bodega, null=False, blank=False, on_delete=models.CASCADE)
    saldo = models.PositiveIntegerField('Saldo')
    def __str__(self):
        txt = '{0} Cantidad: {1}'.format(self.idReferencia, self.saldo)
        return str(txt)
#    estado = models.BooleanField(default=False)


class MovInventario (models.Model):
    idMovimiento = models.AutoField(primary_key=True)
    idReferencia = models.ForeignKey(Referencia, null=False, blank=False, on_delete=models.CASCADE)
    idBodega = models.ForeignKey(Bodega, null=False, blank=False, on_delete=models.CASCADE)
    idTipoUnidadMov = models.ForeignKey(TipoUnidad, null=False, blank=False, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(null=False)
    idTipoMov = models.ForeignKey(TipoMov, null=False, blank=False, on_delete=models.CASCADE)
    fechaMov = models.DateTimeField(auto_now_add=True, editable=False)
    idFactura = models.ForeignKey(Factura, null=False, on_delete=models.CASCADE)
    def __str__(self):
        txt = '{0} To: {1} Cant: {2}'.format(self.idReferencia, self.idBodega, self.cantidad)
        return str(txt)


class FacturaPedido (models.Model):
    idFactura = models.ForeignKey(Factura, null=False, blank=False, on_delete=models.CASCADE)
    idPedido = models.ForeignKey(Pedido, null=False, blank=False, on_delete=models.CASCADE)
    def __str__(self):
        txt = '{} / {}'.format(self.idFactura, self.idPedido)
        return txt


class FacturasMov (models.Model):
    idfactura = models.ForeignKey(Factura, null=False, blank=False, on_delete=models.CASCADE)
    idNumero = models.AutoField(primary_key=True)
    idReferencia = models.ForeignKey(Referencia, null=False, blank=False, on_delete=models.CASCADE)
    fechaPedido = models.DateTimeField(auto_now_add=True, editable=False)
    def __str__(self):
        return str(self.idReferencia)
        # txt = '{0} ({1})'.format(self.idReferencia, self.idfactura)
        # return str(txt)