from django import forms

class EtiquetaForm(forms.Form):
    nueva_etiqueta = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={
        "class": "bg-white text-center text-black fond-bold p-2 rounded w-full border-2 border-cts-secondary",
        "placeholder": "Ingresa nueva etiqueta"
    }))