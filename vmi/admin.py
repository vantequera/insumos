from django.contrib import admin

from vmi.models import Bodega, Factura, FacturaPedido, FacturasMov, Inventario, MovInventario, Pedido, PedidosMov, Proveedor, Referencia, Sede, TipoMov, TipoUnidad

# Register your models here.

admin.site.register(Referencia)
admin.site.register(Proveedor)
admin.site.register(TipoUnidad)
admin.site.register(Sede)
admin.site.register(Bodega)
admin.site.register(Factura)
admin.site.register(TipoMov)
admin.site.register(Pedido)
admin.site.register(PedidosMov)
admin.site.register(Inventario)
admin.site.register(MovInventario)
admin.site.register(FacturaPedido)
admin.site.register(FacturasMov)