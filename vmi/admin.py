from django.contrib import admin
from vmi.models import Billing, City, Country, Department, MovementBilling, Provider, Reference, TypeUnit

admin.site.register(Country)
admin.site.register(Department)
admin.site.register(City)
admin.site.register(TypeUnit)
admin.site.register(Reference)
admin.site.register(Billing)
admin.site.register(MovementBilling)
admin.site.register(Provider)