import site
from django.contrib import admin
from vmi.models import Billing, City, Country, Department, MovementBilling, MovementOrder, Order, Periodo, Provider, ProviderOrder, Reference, TypeUnit


# ======================== Modificadores de Modelos ========================
class PeriodoAdmin(admin.ModelAdmin):
    ordering = ['fecha_inicio']
    list_display = ('__str__', 'estado_del_periodo')


class ReferenceAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'codigo_ean8', 'unique_id')

# ======================== Administrador de Modelos ========================
admin.site.register(Periodo, PeriodoAdmin)
admin.site.register(Country)
admin.site.register(Department)
admin.site.register(City)
admin.site.register(TypeUnit)
admin.site.register(Reference, ReferenceAdmin)
admin.site.register(Billing)
admin.site.register(MovementBilling)
admin.site.register(Provider)
admin.site.register(Order)
admin.site.register(MovementOrder)
admin.site.register(ProviderOrder)