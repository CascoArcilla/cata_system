from django import forms


class AtributesForm(forms.Form):
    def __init__(self, *args, atributes=[], **kwargs):
        super().__init__(*args, **kwargs)

        for index, atribute in enumerate(atributes):
            self.fields[f'atributo_{index+1}'] = forms.CharField(max_length=150, required=True, min_length=3, initial=atribute, label=f"Atributo {index+1}", widget=forms.TextInput(attrs={
                "class": "ct-atributo bg-gray-300 p-1 border-b-1 text-center w-full disabled:bg-gray-500 uppercase"
            }))
