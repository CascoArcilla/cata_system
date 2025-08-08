from django import forms
from ..models import Catador

class CatadorForm(forms.ModelForm):
    class Meta:
        model =  Catador
        fields = "__all__"
        widgets = {
            "usuarioCatador": forms.TextInput( attrs={ "class": "ct-inputs-pos-cata bg-gray-500 text-center w-full p-1 rounded-lg text-white" } ),
            "nombre": forms.TextInput( attrs={ "class": "ct-inputs-pos-cata bg-gray-500 text-center w-full p-1 rounded-lg text-white" } ),
            "apellido": forms.TextInput( attrs={ "class": "ct-inputs-pos-cata bg-gray-500 text-center w-full p-1 rounded-lg text-white" } ),
            "telefono": forms.NumberInput( attrs={ "class": "ct-inputs-pos-cata bg-gray-500 text-center w-full p-1 rounded-lg text-white", "max": "10", "min": "10" } ),
            "correo": forms.EmailInput( attrs={ "class": "ct-inputs-pos-cata bg-gray-500 text-center w-full p-1 rounded-lg text-white" } ),
            "fechaNacimiento": forms.DateTimeInput( attrs={ "class": "ct-inputs-pos-cata bg-gray-500 text-center w-full p-1 rounded-lg text-white", "type": "date", }, format="%d-%m-%y" ),
        }

    def clean(self):
        data_cleand = super().clean()

        phone = data_cleand["telefono"]
        size_phone = len(str(abs(phone)))
        print("tamano de telefono", size_phone)
        if size_phone != 10:
            self.add_error("telefono", "telefono debe tener 10 digitos")
            return data_cleand