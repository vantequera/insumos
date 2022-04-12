from email import message
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

from vmi.models import FacturaDet, FacturaEnc, Proveedor, Referencia
from vmi.forms import ReferenciaForm

# Create your views here.
# ======================== Class Base Views========================
class ReferenciaView(ListView):
    model = Referencia
    template_name = 'vmi/referencias.html'
    context_object_name = 'obj'
    permission_required = 'vmi.view_referencia'

# ======================== Udemy prueba ========================
class ReferenciaView(ListView):
    model = Referencia
    template_name = 'vmi/referencia_list.html'
    context_object_name = 'obj'
    permission_required = 'my_app.view_cliente'


class VistaBaseCreate(SuccessMessageMixin, CreateView):
    context_object_name = 'obj'
    success_message = 'Referencia Nueva'

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)


class VistaBaseUpdate(SuccessMessageMixin, UpdateView):
    context_object_name = 'obj'
    success_message = 'Referencia Actualizada'

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


class ReferenciaNueva(VistaBaseCreate):
    model = Referencia
    template_name = 'vmi/cliente_form.html'
    form_class = ReferenciaForm
    success_url = reverse_lazy('my_app:cliente_list')
    permission_required = 'vmi.add_ref'


class ReferenciaActualizar(VistaBaseUpdate):
    model = Referencia
    template_name = 'vmi/cliente_form.html'
    form_class = ReferenciaForm
    success_url = reverse_lazy('vmi/cliente_list.html')
    permission_required = 'vmi.change_ref'


@login_required(login_url="/login/")
@permission_required('vmi.change_cliente', login_url='/login/')
def refInactivar(request,id):
    referencia = Referencia.object.filter(pk=id).first() # <== O se puede realizar un get() que arroje el primer numero que encuentre

    if request.method == 'POST':
        referencia.estado = not referencia.estado
        referencia.save()
        return HttpResponse('OK')

    return HttpResponse('FAIL')

@login_required(login_url='/login/')
@permission_required('fact.change_facturasenc', login_url='bases:sin_privilegios')
def facturas(request, id=None):
    if request.method == 'POST':
        cliente = request.POST.get('enc_cliente')
        fecha = request.POST.get('fecha')
        cli = Proveedor.objects.get(pk=cliente)

        if not id:
            enc = FacturaEnc(
                cliente = cli,
                fecha = fecha,
            )
            if enc:
                enc.save()
                id = enc.id
        else:
            enc = FacturaEnc.objects.filter(pk=id).first()
            if enc:
                enc.cliente = cli
                enc.save()

        if not id:
            messages.error(request=request, message='Error Inesperado')
            return redirect('fact:factura_list')

    codigo = request.POST.get('codigo')
    cantidad = request.POST.get('cantidad')
    precio = request.POST.get('precio')
    s_total = request.POST.get('sub_total_detalle')
    descuento = request.POST.get('descuento_detalle')
    total = request.POST.get('total_detalle')

    prod = Referencia.objects.get(codigo)
    det = FacturaDet(
        factura = enc,
        producto = prod,
        cantidad = cantidad,
        precio = precio,
        sub_total = s_total,
        descuento = descuento,
        total = total
    )

    if det:
        det.save()

    return redirect('fact:factura_edit', id=id)