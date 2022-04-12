from django.urls import path, include

from api.views import ProductoDetalle, ProductoList


urlpatterns = [
    path('v1/productos/', ProductoList.as_view(), name='listar_ref'),
    path('v1/productos/<str:id>', ProductoDetalle.as_view(), name='detalle_ref')
]