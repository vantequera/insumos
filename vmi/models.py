import datetime
from django.db import models
from django.utils import timezone

# Create your models here.

"""
Modelos con PrimaryKey
ORM -> Object Relational Maping
"""

# Status Choices:
STATUS_CHOICES = [
    ('A', 'Activo'),
    ('I', 'Inhabilitado'),
    ('C', 'Cancelado')
]



class Referencia (models.Model):
    idReferencia = models.AutoField(primary_key=True, null=False)
    nombre = models.CharField(max_length=50, null=False, blank=False)
    ean8 = models.CharField(max_length=50, null=False)
    ean13 = models.CharField(max_length=50)
    ean128 = models.CharField(max_length=50)
    cantidad = models.IntegerField(null=False, blank=False, default=0)

    def __str__(self):
        txt = '{0} ({1})'
        return txt.format(self.nombre.title(), self.cantidad)




class Proveedor (models.Model):
    idProveedor = models.PositiveIntegerField(primary_key=True, null=False)
    nombre = models.CharField(max_length=200, null=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True, editable=False,)
    estado = models.CharField(max_length=1, choices=STATUS_CHOICES)

    def __str__(self):
        return self.nombre
#        txt = '{0} Fecha ({1})'
#        return txt.format(self.nombre, self.fecha_creacion.strftime('%b/%d/%Y - %H:%M'))

    def estado_proveedor(self):  #<== Metodo para ver si esta disponible el proveedor
        return self.estado == 'A'



class TipoUnidad (models.Model):
    idUnidad = models.AutoField(primary_key=True, null=False)
    tipo_unidad = models.CharField(max_length=50, null=False)
#    estado = models.BooleanField(default=False)

    def __str__(self):
        return self.tipo_unidad




class TipoMov (models.Model):
    idTipoMov = models.AutoField(primary_key=True)
    tipo_mov = models.CharField(max_length=50, null=False)
    signo = models.PositiveSmallIntegerField(null=False)
    # estado = models.BooleanField(default=False)

    def __str__(self):
        return self.tipo_mov




class Pais (models.Model):
    idPais = models.IntegerField(primary_key=True, null=False)
    nombre = models.CharField(max_length=50, null=False)
    codigo_dane = models.CharField(max_length=20, null=False)
#    estado = models.CharField(max_length=6)

    def __str__(self):
        return self.nombre



"""
Modelos con PrimaryKey y ForeignKey
"""



class Departamento (models.Model):
    id_departamento = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, null=False)
    id_pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    codigo_dane = models.CharField(max_length=50)
#    estado = models.CharField(max_length=6)

    def __str__(self):
        return self.nombre




class Municipio (models.Model):
    id_municipio = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, null=False)
    id_departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    codigo_dane = models.CharField(max_length=50)
#    estado = models.CharField(max_length=6)

    def __str__(self):
        return self.nombre




class Sede (models.Model):
    idSede = models.PositiveIntegerField(primary_key=True)
    nombre_sede = models.CharField(max_length=50, null=False)
    id_municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)
#    estado = models.CharField(max_length=6)

    def __str__(self):
        return self.nombre_sede
        # txt = '{0} (ID {1})'
        # return txt.format(self.nombre_sede, self.idSede)




class Factura (models.Model):
    idFactura = models.PositiveIntegerField(primary_key=True, null=False)
    idProveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    fechaFactura = models.DateTimeField(auto_now_add=True, editable=False)
#    estado = models.CharField(max_length=6)

    def __str__(self):
        return str(self.idProveedor)
        # txt = '{0} - {1}'.format(self.idProveedor, self.fechaFactura.strftime('%b/%d/%Y'))
        # return txt




class Pedido (models.Model):
    idPedido = models.AutoField(primary_key=True)
    idProveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True, editable=False)
    valor_pedido = models.DecimalField(null=False, blank=False, decimal_places=2, max_digits=13)
#    estado = models.CharField(max_length=6)

    def __str__(self):
        return str(self.idProveedor)

    def es_reciente(self):
        return timezone.now() >= self.fecha_pedido>= timezone.now() - datetime.timedelta(days=15)



class Bodega (models.Model):
    idBodega = models.PositiveIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50, null=False)
    idSede = models.ForeignKey(Sede, on_delete=models.CASCADE)
    id_municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)
#    estado = models.CharField(max_length=6)

    def __str__(self):
        return self.nombre




class SaldoHistorico (models.Model):
    id_referencia = models.AutoField(primary_key=True)
    id_bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE)
    cantidad = models.IntegerField(null=False)
    fecha_corte = models.DateTimeField(null=False)
#    estado = models.CharField(max_length=6)

    def __str__(self):
        return self.id_bodega




class SaldoActual (models.Model):
    id_referencia = models.IntegerField(primary_key=True)
    id_bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE)
    cantidad = models.IntegerField(null=False)
    fecha_mov = models.DateTimeField(auto_now_add=True, editable=False)
#    estado = models.CharField(max_length=6)

    def __str__(self):
        return self.id_bodega




class PedidosMov (models.Model):
    idPedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    idNumero = models.PositiveIntegerField(primary_key=True)
    idReferencia = models.ForeignKey(Referencia, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True, editable=False)
    cantidad = models.PositiveIntegerField(null=False, blank=False, default=0)
    idUnidadCompra = models.ForeignKey(TipoUnidad, on_delete=models.CASCADE)
    valor_de_compra = models.DecimalField(null=False, blank=False, decimal_places=2, max_digits=13)

    def __str__(self):
        txt = '{0} Ref ({1}, {2})'
        return str(txt.format(self.idPedido, self.idReferencia, self.cantidad))





class Inventario (models.Model):
    idReferencia = models.ForeignKey(Referencia, null=False, blank=False, on_delete=models.CASCADE)
    idbodega = models.ForeignKey(Bodega, null=False, blank=False, on_delete=models.CASCADE)
    saldo = models.DecimalField(max_digits=15, decimal_places=3)
#    estado = models.CharField(max_length=6)

    def __str__(self):
        txt = '{0} Cantidad: {1}'.format(self.idReferencia, self.saldo)
        return str(txt)




class MovInventario (models.Model):
    idMovimiento = models.AutoField(primary_key=True)
    idReferencia = models.ForeignKey(Referencia, null=False, blank=False, on_delete=models.CASCADE)
    idBodega = models.ForeignKey(Bodega, null=False, blank=False, on_delete=models.CASCADE)
    idTipoUnidadMov = models.ForeignKey(TipoUnidad, null=False, blank=False, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(null=False)
    idTipoMov = models.ForeignKey(TipoMov, null=False, blank=False, on_delete=models.CASCADE)
    fechaMov = models.DateTimeField(auto_now_add=True, editable=False)
    idFactura = models.ForeignKey(Factura, on_delete=models.CASCADE)

    def __str__(self):
        txt = '{0} To: {1} Cant: {2}'.format(
            self.idReferencia, self.idBodega, self.cantidad)
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