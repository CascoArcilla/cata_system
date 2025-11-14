from django import forms
import re


class ListWordsForm(forms.Form):
    regex = re.compile(r'^[a-zñ]{3,}$')

    def __init__(self, *args, new_words=None, **kwargs):
        super().__init__(*args, **kwargs)
        new_words = new_words or []

        if not new_words:
            self.fields['nombre_palabra'] = forms.CharField(
                label='Nombre de la palabra',
                max_length=255,
                widget=forms.TextInput(attrs={
                    'placeholder': 'Escribe una palabra',
                    'class': 'cts-input-list-word bg-surface-ligt p-1 border-b-1 text-center w-full',
                    'pattern': self.regex.pattern,
                    'title': 'Solo letras minúsculas y la letra ñ, no poner acentos. No se permiten mayúsculas ni caracteres especiales. Mínimo 3 letras',
                })
            )
        else:
            for index, name in enumerate(new_words, start=1):
                self.fields[f'nombre_palabra_{index}'] = forms.CharField(
                    label=f'Palabra {index}',
                    max_length=255,
                    initial=name,
                    widget=forms.TextInput(attrs={
                        'placeholder': 'Escribe una palabra',
                        'class': 'cts-input-list-word bg-surface-ligt p-1 border-b-1 text-center w-full',
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

        if errores:
            raise forms.ValidationError(errores)

        return cleaned_data
