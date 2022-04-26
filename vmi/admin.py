import site
from django.contrib import admin
from vmi.models import (
    Bodega, Ciudad, FacturaDet, FacturaEnc, IngresoP_B, IngresoRefBB,
    IngresoRefPB, Inventario, MovimientoTipo, Pais, Departamento,
    Pedido, Periodo, Proveedor, Referencia, SaldoActual,
    Salida, SalidaRef, Sede, UnidadTipo, IngresoB_B
)


# ======================== StacksInLine ========================
class FacturaInLine(admin.StackedInline):
    model = FacturaDet
    extra = 1


class IngresoInLinePB(admin.StackedInline):
    model = IngresoRefPB
    extra = 1


class IngresoInLineBB(admin.StackedInline):
    model = IngresoRefBB
    extra = 1


class SalidaInLine(admin.StackedInline):
    model = SalidaRef
    extra = 1


# ======================== Modificadores de Modelos ========================
class PaisAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'codigo_pais')


class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'codigo_dane_departamento')


class CiudadAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'codigo_dane', 'departamentos')


class PeriodoAdmin(admin.ModelAdmin):
    ordering = ['fecha_inicio']
    list_display = ('__str__', 'estado_del_periodo')


class ReferenceAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'codigo_ean8', 'unique_id')


class FacturaAdmin(admin.ModelAdmin):
    inlines = [FacturaInLine]
    list_display = ('__str__', 'id', 'fecha_modifica', 'sub_total', 'descuento', 'total')


class Factura2Admin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'cantidad', 'precio', 'sub_total', 'total')


class SedeAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'estado_sede')

class MovimientoTipoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'tipo_de_estado')


# ======================== Administrador de Modelos ========================
admin.site.register(Periodo, PeriodoAdmin)
admin.site.register(Pais, PaisAdmin)
admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(Ciudad, CiudadAdmin)
admin.site.register(UnidadTipo)
admin.site.register(Referencia, ReferenceAdmin)
admin.site.register(Proveedor)
admin.site.register(Pedido)
admin.site.register(MovimientoTipo, MovimientoTipoAdmin)
admin.site.register(FacturaEnc, FacturaAdmin)
admin.site.register(Bodega)
admin.site.register(Sede, SedeAdmin)

# ======================== Inventario ========================
@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'saldo_final', 'tipo_unidad', 'periodo')

# ======================== Saldo Actual ========================
@admin.register(SaldoActual)
class SaldoActualAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'cantidad','temp_alm', 'bodega')

# ======================== Ingreso Proveedor - Bodega ========================
@admin.register(IngresoP_B)
class IngresoAdminPB(admin.ModelAdmin):
    inlines = [IngresoInLinePB]
    list_display = ('__str__', 'factura_prov', 'proveedor')

# ======================== Ingreso Bodega - Bodega ========================
@admin.register(IngresoB_B)
class IngresoAdminBB(admin.ModelAdmin):
    inlines = [IngresoInLineBB]
    list_display = ('__str__', 'pedido', 'bodega_des')

# ======================== Salida ========================
@admin.register(Salida)
class IngresoAdmin(admin.ModelAdmin):
    inlines = [SalidaInLine]
    list_display = ('__str__', 'fecha', 'sede_des')