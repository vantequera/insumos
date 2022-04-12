from rest_framework import serializers

from vmi.models import Referencia


class ProductoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Referencia
        fields = '__all__'