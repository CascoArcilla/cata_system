from django import forms
from tecnicas.models import Palabra


class WordForm(forms.ModelForm):
    nombre_palabra = forms.CharField(
        min_length=3,
        max_length=255,
        error_messages={
            "required": "Parametros requeridos",
            "unique": "Palabra repetida",
            "min_length": "La palabra es muy corta",
            "max_length": "La palabra es muy larga",
        },
        widget=forms.TextInput(attrs={
            "class": "bg-white text-center text-black pb-1 rounded",
            "placeholder": "Ingrese nuevo atributo",
            "oninput": "this.value = this.value.toLowerCase()",
            "required": True,
        })
    )

    class Meta:
        model = Palabra
        fields = ["nombre_palabra"]

    def clean_nombre_palabra(self):
        nombre_palabra = self.cleaned_data.get('nombre_palabra')

        if nombre_palabra:
            nombre_palabra = nombre_palabra.lower().strip()
            nombre_palabra = nombre_palabra.replace(" ", "_")

        if Palabra.objects.filter(nombre_palabra=nombre_palabra).exists():
            raise forms.ValidationError("palabra repetida")

        return nombre_palabra
