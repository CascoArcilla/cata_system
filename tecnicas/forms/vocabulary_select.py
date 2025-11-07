from django import forms
from tecnicas.models import Vocabulario


class VocabularioSelectForm(forms.Form):
    vocabulario = forms.ModelChoiceField(
        queryset=Vocabulario.objects.all(),
        required=True,
        label="Selecciona un vocabulario",
        empty_label="-- Selecciona uno --",
        widget=forms.Select(attrs={
            "class": "w-full border rounded p-4 bg-surface-sweet",
            "id": "vocabulario"
        })
    )
