from django import forms

class EtiquetaForm(forms.Form):
    nueva_etiqueta = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={
        "class": "bg-gray-300 border-b text-center text-black",
        "placeholder": "No repetir etiqueta"
    }))