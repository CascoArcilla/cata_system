from django import forms
from tecnicas.models import Etiqueta


class SesionTagsForm(forms.Form):
    available_struture_tags = {
        "5": ["percepcion nula", "percepcion moderada", "se puede percibir",
              "percepcion intensa", "percepcion total"],
        "7": ["percepcion nula", "ligera percepcion", "percepcion moderada", "se puede percibir", "buena percepcion",
              "percepcion intensa", "percepcion total"],
        "9": ["percepcion nula", "ligera percepcion", "poca percepcion", "percepcion moderada", "se puede percibir", "buena percepcion",
              "percepcion intensa", "percepcion muy intensa", "percepcion total"]
    }

    def __init__(self, *args, longitud=None, tipo_escala: str = None, **kwargs):
        super().__init__(*args, **kwargs)

        if tipo_escala == "estructurada":
            use_tags = self.available_struture_tags[f"{longitud}"]
            for i in range(longitud):
                self.fields[f'segmento_{i+1}'] = forms.ModelChoiceField(queryset=Etiqueta.objects.all(), initial=Etiqueta.objects.get(valor_etiqueta=use_tags[i]), required=True, label=f"segmento {i+1}", empty_label="Selecione opcion", widget=forms.Select(attrs={
                    "class": "ct-select-op p-1 max-sm:w-full bg-white [*]:capitalize"
                }))
        else:
            self.fields['punto_inicial'] = forms.ModelChoiceField(queryset=Etiqueta.objects.all(), initial=Etiqueta.objects.get(valor_etiqueta="percepcion nula"), required=True, label="Punto inicial", empty_label="Selecione opcion", widget=forms.Select(attrs={
                "class": "ct-select-op p-1 max-sm:w-full bg-white [*]:capitalize"
            }))

            self.fields['punto_medio'] = forms.ModelChoiceField(queryset=Etiqueta.objects.all(), initial=Etiqueta.objects.get(valor_etiqueta="se puede percibir"), required=True, label="Punto medio", empty_label="Selecione opcion", widget=forms.Select(attrs={
                "class": "ct-select-op p-1 max-sm:w-full bg-white [*]:capitalize"
            }))

            self.fields['punto_final'] = forms.ModelChoiceField(queryset=Etiqueta.objects.all(), initial=Etiqueta.objects.get(valor_etiqueta="percepcion total"), required=True, label="Punto final", empty_label="Selecione opcion", widget=forms.Select(attrs={
                "class": "ct-select-op p-1 max-sm:w-full bg-white [*]:capitalize"
            }))
