from django import forms
from tecnicas.models import Modalidad


class SesionBasicNappingForm(forms.Form):
    nombre_sesion = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        "class": "bg-white border-b-1 text-center w-full p-1",
        "name": "nombre_sesion",
        "placeholder": "Ej. Mermelada de mango picante"
    }), required=False)

    numero_productos = forms.IntegerField(widget=forms.NumberInput(attrs={
        "class": "bg-white p-1 border-b-1 text-center w-full",
        "placeholder": "Solo números"
    }), required=True)

    numero_catadores = forms.IntegerField(widget=forms.NumberInput(attrs={
        "class": "bg-white p-1 border-b-1 text-center w-full",
        "placeholder": "Solo números"
    }), required=True)

    instrucciones = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        "class": "bg-white border-b-1 text-center w-full p-1",
        "placeholder": "Este campo es opcional"
    }), required=False)

    def __init__(self, *args, **kwargs):
        super(SesionBasicNappingForm, self).__init__(*args, **kwargs)
        names_mod = [
            ("posicionamiento de productos", "posicionamiento de productos"),
            ("sorting", "sorting"),
            ("perfil ultra flash", "perfil ultra flash")
        ]

        self.fields['modalidad'] = forms.CharField(widget=forms.RadioSelect(choices=names_mod, attrs={
            "class": "radio radio-lg radio-info",
            "placeholder": "Seleccione una modalidad",
        }), required=True, initial=names_mod[0])
