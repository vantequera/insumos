import site
from django.contrib import admin
from vmi.models import Ciudad, Factura, MovimientoFactura, Pais, Departamento, MovimientoPedido, Pedido, Periodo, Proveedor, ProveedorPedido, Referencia, UnidadTipo


# ======================== Modificadores de Modelos ========================
class PeriodoAdmin(admin.ModelAdmin):
    ordering = ['fecha_inicio']
    list_display = ('__str__', 'estado_del_periodo')


class ReferenceAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'codigo_ean8', 'unique_id')

# ======================== Administrador de Modelos ========================
admin.site.register(Periodo, PeriodoAdmin)
admin.site.register(Pais)
admin.site.register(Departamento)
admin.site.register(Ciudad)
admin.site.register(UnidadTipo)
admin.site.register(Referencia, ReferenceAdmin)
admin.site.register(Factura)
admin.site.register(MovimientoFactura)
admin.site.register(Proveedor)
admin.site.register(Pedido)
admin.site.register(MovimientoPedido)
admin.site.register(ProveedorPedido)