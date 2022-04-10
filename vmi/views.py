from django.shortcuts import render
from django.views.generic import ListView

from vmi.models import Referencia

# Create your views here.
# ======================== Class Base Views========================
# class ReferenciaView(ListView):
#     model = Referencia
#     template_name = 'vmi/referencias.html'
#     context_object_name = 'obj'
#     permission_required = 'vmi.view_referencia'