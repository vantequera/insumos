from dataclasses import fields
from pyexpat import model
from django.contrib import admin

from vmi.models import Bodega, Factura, FacturaPedido, FacturasMov, Inventario, MovInventario, Pedido, PedidosMov, Proveedor, Referencia, Sede, TipoMov, TipoUnidad


class InventarioInLine(admin.StackedInline):
    model = Inventario
    extra = 2

class ReferenciaAdmin(admin.ModelAdmin):
#    fields = ["IdReferencia", "nombre"]
    inlines = [InventarioInLine]
    list_display = ("idReferencia", "nombre", "cantidad")
    search_fields = ["idReferencia", "ean13"]


class BodegaAdmin(admin.ModelAdmin):
    list_display = ("idSede", "nombre")


class FacturaAdmin(admin.ModelAdmin):
    list_display = ("idProveedor", "idFactura", "fechaFactura")


class FacturasMovAdmin(admin.ModelAdmin):
    list_display = ("idfactura", "idReferencia")

# Register your models here.

admin.site.register(Referencia, ReferenciaAdmin)
admin.site.register(Proveedor)
admin.site.register(TipoUnidad)
admin.site.register(Sede)
admin.site.register(Bodega, BodegaAdmin)
admin.site.register(Factura, FacturaAdmin)
admin.site.register(TipoMov)
admin.site.register(Pedido)
admin.site.register(PedidosMov)
admin.site.register(Inventario)
admin.site.register(MovInventario)
admin.site.register(FacturaPedido)
admin.site.register(FacturasMov, FacturasMovAdmin)