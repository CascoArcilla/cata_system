from django import forms

class EtiquetaForm(forms.Form):
    nueva_etiqueta = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={
        "class": "bg-surface-alter border-b text-center text-black fond-bold p-3",
        "placeholder": "No repetir etiqueta"
    }))