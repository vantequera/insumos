from rest_framework import serializers

from vmi.models import Pedido, Referencia


class ProductoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Referencia
        fields = '__all__'


class PedidoSerializers(serializers.Serializer):
    """ Pedidos Serializers """
    name = serializers.CharField()
    slug_name = serializers.SlugField()
    rides_takens = serializers.IntegerField()
    rides_offered = serializers.IntegerField()
    members_limit = serializers.IntegerField()


pedido = Pedido.objects.latest()

serializer = PedidoSerializers(pedido)

serializer.data