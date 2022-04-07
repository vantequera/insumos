from django.utils.translation import ngettext
from django.contrib import admin, messages
from django.contrib.auth import get_permission_codename

# from vmi.models import (
#     Bodega,
#     Departamento,
#     Factura,
#     FacturaPedido,
#     FacturasMov,
#     Inventario,
#     MovInventario,
#     Municipio,
#     Pais,
#     Pedido,
#     PedidosMov,
#     Proveedor,
#     Referencia,
#     SaldoActual,
#     SaldoHistorico,
#     Sede,
#     TipoMov,
#     TipoUnidad)

# ==== Admin Actions Global ================================================================================================
# Admin actions: <== Aquí es un metodo de cada ModelAdmin
# @admin.action(permissions=['Status'],description='Cancelar Proveedores')
# def cancelar_proveedor(modeladmin, request, queryset):
#     queryset.update(estado='C')


# @admin.action(permissions=['Status'], description='')
# def inhabilitar_proveedor(modeladmin, request, queryset):
#     queryset.update(estado='I')


# ==== Disable Global Actions ===============================================================================================
# Deshabilitar una acción en todo el sitio:
# admin.site.disable_action('delete_selected')


# ==== StackedInline ========================================================================================================

# class InventarioInLine(admin.StackedInline):
#     model = Inventario
#     extra = 2



# ==== ModelAdmin ProveedorAdmin ============================================================================================

# class ProveedorAdmin(admin.ModelAdmin):
#     list_display = ("title_name", "fecha_creacion", "estado")
#     actions = ['cancelar_proveedor', 'inhabilitar_proveedor']

# # Modificar texto en el Admin de Django
#     def title_name(self, obj):
#         return ('{0}'.format(obj.nombre.title()))


#     @admin.action(description='Cancelar Proveedores')
#     def cancelar_proveedor(self, request, queryset):
#         cancelado = queryset.update(estado='C')
#         self.message_user(
#             request,
#             ngettext(
#                 'El proveedor fue cancelado satisfactoriamente.',
#                 'Los proveedores fueron cancelados satisfactoriamente.',
#                 cancelado
#             ) % cancelado, messages.SUCCESS) #<== Cuidado con las comas, lleva cierto orden.


#     @admin.action(description='Inhabilitar un Proveedor', permissions=['change']) #<== Permisions = Usuarios con permisos
#     def inhabilitar_proveedor(self, request, queryset):
#         inhabilitado = queryset.update(estado='I')
#         self.message_user(
#             request,
#             ngettext(
#                 'El proveedor fue inhabilitado exitosamente.',
#                 'Los proveedores fueron inhabilitados exitosamente.',
#                 inhabilitado
#             ), messages.SUCCESS)  #<== Cuidado con las comas, lleva cierto orden.

# Los decoradores en 'Action'
    # @admin.action
    # def make_inactive(self, request, queryset):
    #     queryset.update(is_active=False)

# Deshabilitar condicionamiento de acciones por modelo
    # def get_actions(self, request):
    #     actions = super().get_actions(request)
    #     if request.user.username[0].upper() != 'J':
    #         if 'delete_selected' in actions:
    #             del actions['delete_selected']
    #     return actions

# Puedes verificar si el usuario tiene los permisos
    # def has_admin_permission(self, request):
    #     opts = self.opts
    #     codename = get_permission_codename('change', opts)
    #     return request.user.has_pem('%s.%s' % (opts.app_label, codename))


# ==== ModelAdmin Referencia Admin ====================================================================================

# class ReferenciaAdmin(admin.ModelAdmin):
#     inlines = [InventarioInLine]
#     search_fields = ["idReferencia", "ean13"]
#     list_display = ("title_name", "ean8", "cantidad")

# # Modificar texto en el Admin de Django
#     def title_name(self, obj):
#         return ('{0}'.format(obj.nombre.title()))


# ==== ModelAdmin Bodega Admin =======================================================================================

# class BodegaAdmin(admin.ModelAdmin):
#     list_display = ("nombre", "idSede", "idBodega")

# Modificar texto en el Admin de Django
    # def title_name(self, obj):
    #     return ('{0}'.format(obj.nombre.title()))


# ==== ModelAdmin Factura Admin =======================================================================================

# class FacturaAdmin(admin.ModelAdmin):
#     list_display = ("idProveedor", "idFactura", "fechaFactura")

# Modificar texto en el Admin de Django
    # def title_name(self, obj):
    #     return ('{0}'.format(obj.nombre.title()))


# ==== ModelAdmin Sede Admin =========================================================================================

# class SedeAdmin(admin.ModelAdmin):
#     list_display = ("nombre_sede", "idSede", "id_municipio")

# Modificar texto en el Admin de Django
    # def title_name(self, obj):
    #     return ('{0}'.format(obj.nombre.title()))


# ==== ModelAdmin Facturas Mov Admin =================================================================================

# class FacturasMovAdmin(admin.ModelAdmin):
#     list_display = ("idfactura", "idReferencia")

# Modificar texto en el Admin de Django
    # def title_name(self, obj):
    #     return ('{0}'.format(obj.nombre.title()))


# ==== ModelAdmin Pais Admin =========================================================================================

# class PaisAdmin(admin.ModelAdmin):
#     list_display = ("nombre", "codigo_dane")

# Modificar texto en el Admin de Django
    # def title_name(self, obj):
    #     return ('{0}'.format(obj.nombre.title()))


# ==== ModelAdmin Departamento Admin =================================================================================

# class DepartamentoAdmin(admin.ModelAdmin):
#     list_display = ("nombre", "codigo_dane", "id_pais")

# Modificar texto en el Admin de Django
    # def title_name(self, obj):
    #     return ('{0}'.format(obj.nombre.title()))


# ==== ModelAdmin Municipio Admin =======================================================================================

# class MunicipioAdmin(admin.ModelAdmin):
#     list_display = ("nombre", "codigo_dane", "id_departamento")

# Modificar texto en el Admin de Django
    # def title_name(self, obj):
    #     return ('{0}'.format(obj.nombre.title()))


# ==== ModelAdmin Pedido Admin =========================================================================================

# class PedidoAdmin(admin.ModelAdmin):
#     list_display = ("idProveedor", "es_reciente", "valor_pedido")

# Modificar texto en el Admin de Django
    # def title_name(self, obj):
    #     return ('{0}'.format(obj.nombre.title()))


# ==== ModelAdmin Inventario Admin =======================================================================================

# class InventarioAdmin(admin.ModelAdmin):
#     list_display = ("idReferencia", "saldo")

# Modificar texto en el Admin de Django
    # def title_name(self, obj):
    #     return ('{0}'.format(obj.nombre.title()))


# ==== Register your models here =======================================================================================

# admin.site.register(Referencia, ReferenciaAdmin)
# admin.site.register(Proveedor, ProveedorAdmin)
# admin.site.register(TipoUnidad)
# admin.site.register(Sede, SedeAdmin)
# admin.site.register(Bodega, BodegaAdmin)
# admin.site.register(Factura, FacturaAdmin)
# admin.site.register(TipoMov)
# admin.site.register(Pedido, PedidoAdmin)
# admin.site.register(PedidosMov)
# admin.site.register(Inventario, InventarioAdmin)
# admin.site.register(MovInventario)
# admin.site.register(FacturaPedido)
# admin.site.register(FacturasMov, FacturasMovAdmin)
# admin.site.register(Pais, PaisAdmin)
# admin.site.register(Departamento, DepartamentoAdmin)
# admin.site.register(Municipio, MunicipioAdmin)
# admin.site.register(SaldoActual)
# admin.site.register(SaldoHistorico)