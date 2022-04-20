import site
from django.contrib import admin
from vmi.models import Bodega, Ciudad, Factura, FacturaDet, FacturaEnc, Inventario, MovimientoFactura, MovimientoTipo, Pais, Departamento, MovimientoPedido, Pedido, Periodo, Proveedor, ProveedorPedido, Referencia, Sede, UnidadTipo


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


class FacturaInLine(admin.StackedInline):
    model = FacturaDet
    extra = 3


class Factura2Admin(admin.ModelAdmin):
    list_display = ('__str__', 'cantidad', 'precio', 'sub_total', 'total')


class MovimientoTipoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'tipo_de_estado')


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
admin.site.register(MovimientoTipo, MovimientoTipoAdmin)
admin.site.register(MovimientoPedido)
admin.site.register(ProveedorPedido)
admin.site.register(FacturaEnc, FacturaAdmin)
admin.site.register(FacturaDet, Factura2Admin)
admin.site.register(Bodega)
admin.site.register(Sede)

@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'saldo_final', 'tipo_unidad', 'periodo')