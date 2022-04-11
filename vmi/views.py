from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required, permission_required

from vmi.models import Referencia
from vmi.forms import ReferenciaForm

# Create your views here.
# ======================== Class Base Views========================
# class ReferenciaView(ListView):
#     model = Referencia
#     template_name = 'vmi/referencias.html'
#     context_object_name = 'obj'
#     permission_required = 'vmi.view_referencia'

# ======================== Udemy prueba ========================
# class ReferenciaView(ListView):
#     model = Referencia
#     template_name = 'vmi/referencia_list.html'
#     context_object_name = 'obj'
#     permission_required = 'my_app.view_cliente'


# class VistaBaseCreate(SuccessMessageMixin, CreateView):
#     context_object_name = 'obj'
#     success_message = 'Referencia Nueva'

#     def form_valid(self, form):
#         form.instance.uc = self.request.user
#         return super().form_valid(form)


# class VistaBaseUpdate(SuccessMessageMixin, UpdateView):
#     context_object_name = 'obj'
#     success_message = 'Referencia Actualizada'

#     def form_valid(self, form):
#         form.instance.um = self.request.user.id
#         return super().form_valid(form)


# class ReferenciaNueva(VistaBaseCreate):
#     model = Referencia
#     template_name = 'vmi/cliente_form.html'
#     form_class = ReferenciaForm
#     success_url = reverse_lazy('my_app:cliente_list')
#     permission_required = 'vmi.add_ref'


# class ReferenciaActualizar(VistaBaseUpdate):
#     model = Referencia
#     template_name = 'vmi/cliente_form.html'
#     form_class = ReferenciaForm
#     success_url = reverse_lazy('vmi/cliente_list.html')
#     permission_required = 'vmi.change_ref'


# @login_required(login_url="/login/")
# @permission_required('vmi.change_cliente', login_url='/login/')
# def refInactivar(request,id):
#     referencia = Referencia.object.filter(pk=id).first()

#     if request.method == 'POST':
#         referencia.estado = not referencia.estado
#         referencia.save()
#         return HttpResponse('OK')

#     return HttpResponse('FAIL')