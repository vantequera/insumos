from django.contrib import admin

from vmi.models import Bodega, Departamento, Factura, FacturaPedido, FacturasMov, Inventario, MovInventario, Municipio, Pais, Pedido, PedidosMov, Proveedor, Referencia, SaldoActual, SaldoHistorico, Sede, TipoMov, TipoUnidad


class InventarioInLine(admin.StackedInline):
    model = Inventario
    extra = 2

class ReferenciaAdmin(admin.ModelAdmin):
    inlines = [InventarioInLine]
    search_fields = ["idReferencia", "ean13"]
    list_display = ("ean8", "nombre", "cantidad")


class BodegaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "idSede", "idBodega")


class FacturaAdmin(admin.ModelAdmin):
    list_display = ("idProveedor", "idFactura", "fechaFactura")


class SedeAdmin(admin.ModelAdmin):
    list_display = ("nombre_sede", "idSede", "id_municipio")


class FacturasMovAdmin(admin.ModelAdmin):
    list_display = ("idfactura", "idReferencia")


class PaisAdmin(admin.ModelAdmin):
    list_display = ("nombre", "codigo_dane")


class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "codigo_dane", "id_pais")


class MunicipioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "codigo_dane", "id_departamento")


class PedidoAdmin(admin.ModelAdmin):
    list_display = ("idProveedor", "es_reciente")

class InventarioAdmin(admin.ModelAdmin):
    list_display = ("idReferencia", "saldo")


# Register your models here.

admin.site.register(Referencia, ReferenciaAdmin)
admin.site.register(Proveedor)
admin.site.register(TipoUnidad)
admin.site.register(Sede, SedeAdmin)
admin.site.register(Bodega, BodegaAdmin)
admin.site.register(Factura, FacturaAdmin)
admin.site.register(TipoMov)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(PedidosMov)
admin.site.register(Inventario, InventarioAdmin)
admin.site.register(MovInventario)
admin.site.register(FacturaPedido)
admin.site.register(FacturasMov, FacturasMovAdmin)
admin.site.register(Pais, PaisAdmin)
admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(Municipio, MunicipioAdmin)
admin.site.register(SaldoActual)
admin.site.register(SaldoHistorico)