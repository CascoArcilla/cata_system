from django import forms

from ..models import TipoEscala

class SesionFirtsForm(forms.Form):
    nombre_sesion = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        "class": "bg-gray-200 border-b-1 text-center w-full p-1",
        "name": "nombre_sesion",
        "placeholder": "Ej. Mermelada de mango picante"
    }), required=True)

    numero_productos = forms.IntegerField(widget=forms.NumberInput(attrs={
        "class": "bg-gray-200 p-1 border-b-1 text-center w-full",
        "placeholder": "Solo números"
    }), required=True)

    numero_jueces = forms.IntegerField(widget=forms.NumberInput(attrs={
        "class": "bg-gray-200 p-1 border-b-1 text-center w-full",
        "placeholder": "Solo números"
    }), required=True)
    
    numero_repeticiones = forms.IntegerField(widget=forms.NumberInput(attrs={
        "class": "bg-gray-200 p-1 border-b-1 text-center w-full",
        "placeholder": "Solo números"
    }), required=True)

    tipo_escala = forms.ModelChoiceField(queryset=TipoEscala.objects.all(), required=True, widget=forms.RadioSelect(attrs={
        "class":"uppercase text-lg tracking-wider font-medium p-2 px-4 active:px-5 transition-all rounded-xl bg-blue-500 text-white",
    }))

    tamano_escala = forms.IntegerField(widget=forms.NumberInput(attrs={
        "class": "bg-gray-200 p-1 border-b-1 text-center w-full",
    }), required=True, min_value=5, max_value=9)