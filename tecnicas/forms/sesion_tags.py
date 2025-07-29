from django import forms
from django.shortcuts import redirect
from django.urls import reverse

from ..models import Etiqueta

class SesionTagsForm(forms.Form):
    def __init__(self, *args, segmentos=None, **kwargs):
        super().__init__(*args, **kwargs)

        for i in range(segmentos):
            self.fields[f'segmento_{i}'] = forms.ModelChoiceField(queryset=Etiqueta.objects.all(), required=True,label=f"segmento {i+1}", empty_label="Selecione opcion", widget=forms.Select(attrs={
                "class":"ct-select-op p-1 rounded bg-gray-200 [*]:capitalize"
            }))