"""insumos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import ReferenciaNueva, ReferenciaActualizar, refInactivar


# ======================== URL Patterns de udemy ========================
urlpatterns = [
    path('', ReferenciaNueva.as_view(), name='referencia_list'),
    path('referencia/new', ReferenciaNueva.as_view(), name='referencia_new'),
    path('referencia/<int:pk>', ReferenciaActualizar.as_view(), name='referencia_edit'),
    path('referencia/estado/<int:pk>', refInactivar, name='inactivar_ref')
]