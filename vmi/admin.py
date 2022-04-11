import site
from django.contrib import admin
from vmi.models import Bodega, Ciudad, Factura, FacturaDet, FacturaEnc, MovimientoFactura, Pais, Departamento, MovimientoPedido, Pedido, Periodo, Proveedor, ProveedorPedido, Referencia, Sede, UnidadTipo


# ======================== Modificadores de Modelos ========================
class PaisAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'codigo_pais')


class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'codigo_dane_departamento')


class CiudadAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'codigo_dane_ciudad')


class PeriodoAdmin(admin.ModelAdmin):
    ordering = ['fecha_inicio']
    list_display = ('__str__', 'estado_del_periodo')


class ReferenceAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'codigo_ean8', 'unique_id')


class FacturaAdmin(admin.ModelAdmin):
    pass


class Factura2Admin(admin.ModelAdmin):
    pass

# ======================== Administrador de Modelos ========================
admin.site.register(Periodo, PeriodoAdmin)
admin.site.register(Pais, PaisAdmin)
admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(Ciudad, CiudadAdmin)
admin.site.register(UnidadTipo)
admin.site.register(Referencia, ReferenceAdmin)
admin.site.register(Factura)
admin.site.register(MovimientoFactura)
admin.site.register(Proveedor)
admin.site.register(Pedido)
admin.site.register(MovimientoPedido)
admin.site.register(ProveedorPedido)
admin.site.register(FacturaEnc, FacturaAdmin)
admin.site.register(FacturaDet, Factura2Admin)
admin.site.register(Bodega)
admin.site.register(Sede)