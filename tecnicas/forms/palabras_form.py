from django import forms

class PalabrasForm(forms.Form):
    def __init__(self, *args, codes = [], **kwargs):
        super().__init__(*args, **kwargs)

        for index, code in enumerate(codes):
            self.fields[f'producto_{index+1}'] = forms.CharField(max_length=3, required=True, min_length=3, initial=code, label=f"codigo {index+1}", widget=forms.TextInput(attrs={
                "class": "ct-palabra bg-gray-300 p-1 border-b-1 text-center w-full disabled:bg-gray-500 uppercase"
            }))