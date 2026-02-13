from django import forms
from tecnicas.models import TipoEscala, EstiloPalabra


class SesionBasicForm(forms.Form):
    sizes_structure = [5, 7, 9]
    sizes_continue = [9, 13, 15]
    options = [
        ("atributos", "atributos"),
        ("vocabulario", "vocabulario")
    ]
    type_scales = [
        ("estructurada", "estructurada"),
        ("continua", "continua")
    ]

    nombre_sesion = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        "class": "bg-white border-b-1 text-center w-full p-1",
        "name": "nombre_sesion",
        "placeholder": "Ej. Mermelada de mango picante"
    }), required=False)

    numero_productos = forms.IntegerField(widget=forms.NumberInput(attrs={
        "class": "bg-white p-1 border-b-1 text-center w-full",
        "placeholder": "Solo números"
    }), required=True)

    numero_catadores = forms.IntegerField(widget=forms.NumberInput(attrs={
        "class": "bg-white p-1 border-b-1 text-center w-full",
        "placeholder": "Solo números"
    }), required=True)

    numero_repeticiones = forms.IntegerField(widget=forms.NumberInput(attrs={
        "class": "bg-white p-1 border-b-1 text-center w-full",
        "placeholder": "Solo números"
    }), required=True)

    instrucciones = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        "class": "bg-white border-b-1 text-center w-full p-1",
        "placeholder": "Este campo es opcional"
    }), required=False)

    def __init__(self, *args, initial_conf: dict = None, **kwargs):
        super().__init__(*args, **kwargs)

        if initial_conf is None:
            initial_conf = {}

        self.fields['estilo_palabras'] = forms.ChoiceField(choices=self.options, widget=forms.RadioSelect(attrs={
            "class": "uppercase text-lg tracking-wider font-medium p-2 px-4 active:px-5 transition-all rounded-xl bg-blue-500 text-white",
        }), required=True, initial=self.options[0])

        self.fields['tipo_escala'] = forms.ChoiceField(choices=self.type_scales, widget=forms.RadioSelect(attrs={
            "class": "uppercase text-lg tracking-wider font-medium p-2 px-4 active:px-5 transition-all rounded-xl bg-blue-500 text-white",
        }), required=True, initial=self.type_scales[0])

        self.fields['tamano_escala'] = forms.IntegerField(widget=forms.HiddenInput(attrs={
            "class": "cts-size-input",
        }), required=True)

        if "numero_catadores" in initial_conf:
            self.fields["numero_catadores"].initial = initial_conf["numero_catadores"]

        if "numero_repeticiones" in initial_conf:
            self.fields["numero_repeticiones"].initial = initial_conf["numero_repeticiones"]

    def clean(self):
        data_clean = super().clean()
        name_scale = data_clean.get("tipo_escala")
        scale: TipoEscala

        try:
            scale = TipoEscala.objects.get(nombre_escala=name_scale)
        except TipoEscala.DoesNotExist:
            self.add_error("tipo_escala", "Escala no valida")
            return data_clean

        data_clean["tipo_escala"] = scale
        size_scale = data_clean.get("tamano_escala")

        if scale.nombre_escala == "estructurada" and not self.sizes_structure.__contains__(size_scale):
            self.add_error("tamano_escala", "El tamaño de la escala no aplica")
        elif scale.nombre_escala == "continua" and not self.sizes_continue.__contains__(size_scale):
            self.add_error("tamano_escala", "El tamaño de la escala no aplica")
