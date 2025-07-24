from django import forms

from ..models import TipoEscala

class SesionFirtsForm(forms.Form):
    nombre_sesion = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        "class": "bg-gray-200 border-b-1 text-center w-full p-1",
        "name": "nombre_sesion",
        "placeholder": "Ej. Mermelada de mango picante"
    }), required=False)

    numero_productos = forms.IntegerField(widget=forms.NumberInput(attrs={
        "class": "bg-gray-200 p-1 border-b-1 text-center w-full",
        "placeholder": "Solo números"
    }), required=True)

    numero_jueces = forms.IntegerField(widget=forms.NumberInput(attrs={
        "class": "bg-gray-200 p-1 border-b-1 text-center w-full",
        "placeholder": "Solo números"
    }), required=True)
    
    numero_repeticiones = forms.IntegerField(widget=forms.NumberInput(attrs={
        "class": "bg-gray-200 p-1 border-b-1 text-center w-full",
        "placeholder": "Solo números"
    }), required=True)

    tipo_escala = forms.ModelChoiceField(queryset=TipoEscala.objects.all(), widget=forms.RadioSelect(attrs={
        "class":"uppercase text-lg tracking-wider font-medium p-2 px-4 active:px-5 transition-all rounded-xl bg-blue-500 text-white",
    }), required=True, initial=TipoEscala.objects.first())

    tamano_escala = forms.IntegerField(widget=forms.NumberInput(attrs={
        "class": "bg-gray-200 p-1 border-b-1 text-center w-full",
    }), required=True, min_value=5)

    def clean(self):
        data_clean = super().clean()

        sizes_estruturada = [5, 7, 9]
        sizes_continua = [9, 12, 15]

        escala = data_clean.get("tipo_escala")

        if escala and not isinstance(escala, TipoEscala):
            try:
                escala = TipoEscala.objects.get(pk=escala)
            except (ValueError, TipoEscala.DoesNotExist):
                self.add_error("tipo_escala", "Escala no valida")
                return data_clean

        tamano_escala = data_clean.get("tamano_escala")

        if escala.nombre_escala == "estructurada" and not sizes_estruturada.__contains__(tamano_escala):
            self.add_error("tamano_escala", "El tamaño de la escala no aplica")
        elif escala.nombre_escala == "continua" and not sizes_continua.__contains__(tamano_escala):
            self.add_error("tamano_escala", "El tamaño de la escala no aplica")
        else:
            self.add_error("tipo_escala", "Escala no valida")