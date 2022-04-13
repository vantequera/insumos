from django.urls import path, include

from api.views import ProductoDetalle, ProductoList


urlpatterns = [
    path('', ProductoList.as_view(), name='listar_ref'),
    path('<str:unique_id>', ProductoDetalle.as_view(), name='detalle_ref')
]