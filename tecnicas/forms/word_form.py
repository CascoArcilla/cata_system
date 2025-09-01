from django import forms

from ..models import Palabra


class WordForm(forms.ModelForm):
    class Meta:
        model = Palabra
        fields = ["nombre_palabra"]

        labels = {
            "nombre_palabra": "nombre_palabra"
        }

        widgets = {
            "nombre_palabra": forms.TextInput(attrs={
                "class": "bg-gray-300 border-b text-center text-black pb-1 rounded",
                "placeholder": "Ingrese palabra",
                "oninput": "this.value = this.value.toLowerCase()"
            })
        }

        error_messages = {
            "nombre_palabra": {
                "required": "parametros requeridos",
                "unique": "palabra repetida"
            }
        }

    def clean_nombre_palabra(self):
        nombre_palabra = self.cleaned_data.get('nombre_palabra')

        if nombre_palabra:
            nombre_palabra = nombre_palabra.lower().strip()

        return nombre_palabra
