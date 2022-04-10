from django import forms

from vmi.models import Referencia




class ReferenciaForm(forms.ModelForm):
    email = forms.EmailField(max_length=50)

    class Meta:
        model = Referencia
#         fields = ['']  <== Se usa para selecionar campos a mostrar y su orden
#         exclude = [] <== Se usa para quitar campos de los formularios
#         widget = {}  <== Se usa para mostrar campos en widget

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            # Agregando un atributo item por item creado en su clase
            self.fields[field].widget.attrs.update({
                'class': 'form_control'
            })