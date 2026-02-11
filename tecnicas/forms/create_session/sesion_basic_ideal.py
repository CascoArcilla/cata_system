from django import forms


class SesionBasicIdealForm(forms.Form):
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

    instrucciones = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        "class": "bg-white border-b-1 text-center w-full p-1",
        "placeholder": "Este campo es opcional"
    }), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        options = [
            ("atributos", "atributos"),
            ("vocabulario", "vocabulario")
        ]

        self.fields['estilo_palabras'] = forms.ChoiceField(choices=options, widget=forms.RadioSelect(attrs={
            "class": "uppercase text-lg tracking-wider font-medium p-2 px-4 active:px-5 transition-all rounded-xl bg-blue-500 text-white",
        }), required=True, initial=options[0])
