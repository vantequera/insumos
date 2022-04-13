from django.shortcuts import render
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from api.serializers import ProductoSerializer
from vmi.models import Referencia

# Create your views here.

class ProductoList(APIView):

    def get(self, request):
        prod = Referencia.objects.all()
        data = ProductoSerializer(prod, many=True).data
        return Response(data)


class ProductoDetalle(APIView):

    def get(self, request, unique_id):
        prod = get_object_or_404(Referencia, unique_id=unique_id) #<== Busquedas complejas funcionan como AND y OR
        data = ProductoSerializer(prod).data
        return Response(data)