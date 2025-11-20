from django import forms
from tecnicas.models import TipoEscala


class SesionBasicPFForm(forms.Form):
    nombre_sesion = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        "class": "bg-surface-ligt border-b-1 text-center w-full p-1",
        "name": "nombre_sesion",
        "placeholder": "Ej. Mermelada de mango picante"
    }), required=False)

    numero_productos = forms.IntegerField(widget=forms.NumberInput(attrs={
        "class": "bg-surface-ligt p-1 border-b-1 text-center w-full",
        "placeholder": "Solo números"
    }), required=True)

    numero_catadores = forms.IntegerField(widget=forms.NumberInput(attrs={
        "class": "bg-surface-ligt p-1 border-b-1 text-center w-full",
        "placeholder": "Solo números"
    }), required=True)

    numero_repeticiones = forms.IntegerField(widget=forms.NumberInput(attrs={
        "class": "bg-surface-ligt p-1 border-b-1 text-center w-full",
        "placeholder": "Solo números"
    }), required=True)

    instrucciones = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        "class": "bg-surface-ligt border-b-1 text-center w-full p-1",
        "placeholder": "Este campo es opcional"
    }), required=False)
