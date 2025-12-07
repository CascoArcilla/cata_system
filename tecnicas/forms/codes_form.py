from django import forms


class CodesForm(forms.Form):
    def __init__(self, *args, codes=[], **kwargs):
        super().__init__(*args, **kwargs)

        for index, code in enumerate(codes):
            self.fields[f'producto_{index+1}'] = forms.CharField(max_length=3, required=True, min_length=3, initial=code, label=f"codigo {index+1}", widget=forms.TextInput(attrs={
                "class": "ct-code bg-surface-ligt p-1 border-b-1 text-center w-full disabled:bg-surface-general uppercase"
            }))

    def clean(self):
        cleaned_data = super().clean()
        # Convert all product codes to uppercase
        for field_name, value in cleaned_data.items():
            if field_name.startswith('producto_') and value:
                cleaned_data[field_name] = value.upper()
        return cleaned_data
