from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db.models import Sum
from django.utils import timezone

from vmi.models import FacturaDet, FacturaEnc, Referencia, Inventario, Periodo

############################################################################
############################################################################
# Los signals no pueden ir fuera del modelo, aun no se como trabajarlo fuera
############################################################################
############################################################################

# # === Signals del área de facturación ========================
# @receiver(post_save, sender=FacturaDet)
# def detalle_fac_guardar(sender, instance, **kwargs):
#     factura_id = instance.factura.id
#     # referencia_id = instance.producto.id

#     enc = FacturaEnc.objects.get(pk=factura_id)
#     if enc:
#         sub_total = FacturaDet.objects.filter(factura=factura_id).aggregate(sub_total=Sum('sub_total')).get('sub_total', 0.00)
#         descuento = FacturaDet.objects.filter(factura=factura_id).aggregate(descuento=Sum('descuento')).get('descuento', 0.00)
#         enc.sub_total = sub_total
#         enc.descuento = descuento
#         enc.total = sub_total - descuento
#         enc.save()

    # prod = Referencia.objects.get(pk=referencia_id)
    # if prod:
    #     cantidad = int(prod.existencia) - int(instance.cantidad)
    #     prod.existencia = cantidad
    #     prod.save()

# post_save.connect(detalle_fac_guardar, FacturaDet)


# === Signals de Periodo model ========================
# def cerrar_periodo(sender, instance, **kwargs):
#     periodo = instance.id
#     inventario = Inventario.objects.filter(periodo=periodo)
#     inventario.periodo = False
#     inventario.save()
#     print(inventario)


# post_save.connect(cerrar_periodo, sender=Periodo)

# # def cierre_de_estado(self):
# #     fecha_cierre = timezone.now() >= self.fecha_fin>= timezone.now() - datetime.timedelta(days=7)
# #     if fecha_cierre:
# #         cambio = self.estado = False
# #         return cambio


# @receiver(pre_save, sender=Inventario)
# def saldoAnterior(sender, instance, **kwargs):
#     mi_inventario = instance.saldo_inicial