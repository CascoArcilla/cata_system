from django import forms
from tecnicas.models import TipoEscala, EstiloPalabra


class SesionBasicForm(forms.Form):
    sizes_structure = [5, 7, 9]
    sizes_continue = [9, 13, 15]

    nombre_sesion = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        "class": "bg-surface-ligt border-b-1 text-center w-full p-1",
        "name": "nombre_sesion",
        "placeholder": "Ej. Mermelada de mango picante"
    }), required=False)

    numero_productos = forms.IntegerField(widget=forms.NumberInput(attrs={
        "class": "bg-surface-ligt p-1 border-b-1 text-center w-full",
        "placeholder": "Solo números"
    }), required=True)

    numero_catadores = forms.IntegerField(widget=forms.NumberInput(attrs={
        "class": "bg-surface-ligt p-1 border-b-1 text-center w-full",
        "placeholder": "Solo números"
    }), required=True)

    numero_repeticiones = forms.IntegerField(widget=forms.NumberInput(attrs={
        "class": "bg-surface-ligt p-1 border-b-1 text-center w-full",
        "placeholder": "Solo números"
    }), required=True)

    instrucciones = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        "class": "bg-surface-ligt border-b-1 text-center w-full p-1",
        "placeholder": "Este campo es opcional"
    }), required=False)

    def __init__(self, *args, initial_conf: dict = None, **kwargs):
        super().__init__(*args, **kwargs)

        if initial_conf is None:
            initial_conf = {}

        options = [
            ("atributos", "atributos"),
            ("vocabulario", "vocabulario")
        ]

        self.fields['estilo_palabras'] = forms.ChoiceField(choices=options, widget=forms.RadioSelect(attrs={
            "class": "uppercase text-lg tracking-wider font-medium p-2 px-4 active:px-5 transition-all rounded-xl bg-blue-500 text-white",
        }), required=True, initial=options[0])

        self.fields['tipo_escala'] = forms.ModelChoiceField(queryset=TipoEscala.objects.all(), widget=forms.RadioSelect(attrs={
            "class": "uppercase text-lg tracking-wider font-medium p-2 px-4 active:px-5 transition-all rounded-xl bg-blue-500 text-white",
        }), required=True, initial=TipoEscala.objects.first())

        self.fields['tamano_escala'] = forms.IntegerField(widget=forms.HiddenInput(attrs={
            "class": "cts-size-input",
        }), required=True)

        if "numero_catadores" in initial_conf:
            self.fields["numero_catadores"].initial = initial_conf["numero_catadores"]

        if "numero_repeticiones" in initial_conf:
            self.fields["numero_repeticiones"].initial = initial_conf["numero_repeticiones"]

    def clean(self):
        data_clean = super().clean()
        escala = data_clean.get("tipo_escala")

        if escala and not isinstance(escala, TipoEscala):
            try:
                escala = TipoEscala.objects.get(pk=escala)
            except (ValueError, TipoEscala.DoesNotExist):
                print("Escala no valida")
                self.add_error("tipo_escala", "Escala no valida")
                return data_clean

        tamano_escala = data_clean.get("tamano_escala")

        if escala.nombre_escala == "estructurada" and not self.sizes_structure.__contains__(tamano_escala):
            self.add_error("tamano_escala", "El tamaño de la escala no aplica")
        elif escala.nombre_escala == "continua" and not self.sizes_continue.__contains__(tamano_escala):
            self.add_error("tamano_escala", "El tamaño de la escala no aplica")
