from django import forms
from tecnicas.models import Etiqueta


class SesionTagsForm(forms.Form):
    available_struture_tags = {
        "5": ["percepción nula", "percepción moderada", "se puede percibir",
              "percepción intensa", "percepción total"],
        "7": ["percepción nula", "ligera percepción", "percepción moderada", "se puede percibir", "buena percepción",
              "percepción intensa", "percepción total"],
        "9": ["percepción nula", "ligera percepción", "poca percepción", "percepción moderada", "se puede percibir", "buena percepción",
              "percepción intensa", "percepción muy intensa", "percepción total"]
    }

    available_cotinue_tags = {
        "start": "intensidad nula",
        "middle": "intensidad moderada",
        "end": "intensidad fuerte"
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
            self.fields['punto_inicial'] = forms.ModelChoiceField(queryset=Etiqueta.objects.all(), initial=Etiqueta.objects.get(valor_etiqueta=self.available_cotinue_tags["start"]), required=True, label="Punto inicial", empty_label="Selecione opcion", widget=forms.Select(attrs={
                "class": "ct-select-op p-1 max-sm:w-full bg-white [*]:capitalize"
            }))

            self.fields['punto_medio'] = forms.ModelChoiceField(queryset=Etiqueta.objects.all(), initial=Etiqueta.objects.get(valor_etiqueta=self.available_cotinue_tags["middle"]), required=True, label="Punto medio", empty_label="Selecione opcion", widget=forms.Select(attrs={
                "class": "ct-select-op p-1 max-sm:w-full bg-white [*]:capitalize"
            }))

            self.fields['punto_final'] = forms.ModelChoiceField(queryset=Etiqueta.objects.all(), initial=Etiqueta.objects.get(valor_etiqueta=self.available_cotinue_tags["end"]), required=True, label="Punto final", empty_label="Selecione opcion", widget=forms.Select(attrs={
                "class": "ct-select-op p-1 max-sm:w-full bg-white [*]:capitalize"
            }))
