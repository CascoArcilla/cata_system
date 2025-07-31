from django import forms
from django.shortcuts import redirect
from django.urls import reverse

from ..models import Etiqueta

class SesionTagsForm(forms.Form):
    def __init__(self, *args, longitud=None, tipo_escala:str=None, **kwargs):
        super().__init__(*args, **kwargs)

        if tipo_escala == "estructurada":
            for i in range(longitud):
                self.fields[f'segmento_{i}'] = forms.ModelChoiceField(queryset=Etiqueta.objects.all(), required=True,label=f"segmento {i+1}", empty_label="Selecione opcion", widget=forms.Select(attrs={
                    "class":"ct-select-op p-1 rounded bg-gray-200 [*]:capitalize"
                }))
        else:
            self.fields['punto_inicial'] = forms.ModelChoiceField(queryset=Etiqueta.objects.all(), required=True, label="Punto inicial", empty_label="Selecione opcion", widget=forms.Select(attrs={
                    "class":"ct-select-op p-1 rounded bg-gray-200 [*]:capitalize"
                }))
            
            self.fields['punto_medio'] = forms.ModelChoiceField(queryset=Etiqueta.objects.all(), required=True, label="Punto medio", empty_label="Selecione opcion", widget=forms.Select(attrs={
                    "class":"ct-select-op p-1 rounded bg-gray-200 [*]:capitalize"
                }))
            
            self.fields['punto_final'] = forms.ModelChoiceField(queryset=Etiqueta.objects.all(), required=True, label="Punto final", empty_label="Selecione opcion", widget=forms.Select(attrs={
                    "class":"ct-select-op p-1 rounded bg-gray-200 [*]:capitalize"
                }))