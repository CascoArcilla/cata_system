from django import forms
import re


class ListWordsForm(forms.Form):
    # Regex para validar palabras: solo letras minúsculas y la letra ñ, mínimo 3 caracteres, con espacios
    regex = re.compile(r'^[a-zñ ]{3,}$')

    def __init__(self, *args, new_words=None, **kwargs):
        super().__init__(*args, **kwargs)

        if not new_words:
            self.fields['nombre_palabra'] = forms.CharField(
                label='Nombre de atributo',
                max_length=255,
                widget=forms.TextInput(attrs={
                    'placeholder': 'Escribe un atributo',
                    'class': 'cts-input-list-word bg-white p-1 border-b-1 text-center w-full',
                    'pattern': self.regex.pattern,
                    'title': 'Solo letras minúsculas y la letra ñ. No se permiten mayúsculas ni caracteres especiales. Mínimo 3 letras'
                })
            )
        else:
            for index, name in enumerate(new_words, start=1):
                self.fields[f'palabra_{index}'] = forms.CharField(
                    label=f'Atributo {index}',
                    max_length=255,
                    initial=name,
                    widget=forms.TextInput(attrs={
                        'placeholder': 'Escribe un atributo',
                        'class': 'cts-input-list-word bg-white p-1 border-b-1 text-center w-full',
                        'pattern': self.regex.pattern,
                        'title': 'Solo letras minúsculas y la letra ñ. No se permiten mayúsculas ni caracteres especiales.'
                    })
                )

    def clean(self):
        cleaned_data = super().clean()
        errores = []

        for field_name, value in cleaned_data.items():
            if not self.regex.match(value):
                errores.append(f"'{value}' contiene caracteres no permitidos.")
            elif len(value) > 255:
                errores.append(f"'{value}' excede los 255 caracteres.")
            else:
                cleaned_data[field_name] = value.lower().strip().replace(" ", "_")

        if errores:
            raise forms.ValidationError(errores)

        return cleaned_data
