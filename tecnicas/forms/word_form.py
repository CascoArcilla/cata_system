from django import forms

from ..models import Palabra


class WordForm(forms.ModelForm):
    nombre_palabra = forms.CharField(
        min_length=3,
        max_length=255,
        error_messages={
            "required": "parametros requeridos",
            "unique": "palabra repetida",  # Ojo: 'unique' lo maneja ModelForm, no aquí
            "min_length": "la palabra es muy corta",
            "max_length": "la palabra es muy larga",
        },
        widget=forms.TextInput(attrs={
            "class": "bg-gray-300 border-b text-center text-black pb-1 rounded",
            "placeholder": "Ingrese palabra",
            "oninput": "this.value = this.value.toLowerCase()",
        })
    )

    class Meta:
        model = Palabra
        fields = ["nombre_palabra"]

    def clean_nombre_palabra(self):
        nombre_palabra = self.cleaned_data.get('nombre_palabra')

        if nombre_palabra:
            nombre_palabra = nombre_palabra.lower().strip()

        if Palabra.objects.filter(nombre_palabra=nombre_palabra).exists():
            raise forms.ValidationError("palabra repetida")

        return nombre_palabra
