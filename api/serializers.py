from rest_framework import serializers

from vmi.models import PedidoBB, Referencia


class ProductoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Referencia
        fields = '__all__'


#####################################################
################# Clase de API Rest #################

# class PedidoSerializers(serializers.Serializer):
#     """ Pedidos Serializers """
#     name = serializers.CharField()
#     slug_name = serializers.SlugField()
#     rides_takens = serializers.IntegerField()
#     rides_offered = serializers.IntegerField()
#     members_limit = serializers.IntegerField()


# pedido = Pedido.objects.latest()

# serializer = PedidoSerializers(pedido)

# serializer.data