from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, EmailValidator


class CatadorForm(forms.Form):
    styles_input = "ct-inputs-pos-cata bg-white text-center w-full p-1 rounded-lg text-black disabled:bg-cts-secondary"

    nombre_usuario = forms.CharField(
        label="Nombre de usuario",
        max_length=30,
        min_length=5,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^(?![0-9._])[A-Za-z0-9._]+$',
                message=(
                    "El nombre de usuario debe iniciar con una letra y solo puede "
                    "contener letras, números, puntos y guiones bajos."
                ),
                code='invalid_username'
            )
        ],
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ej. mario_hugo23",
                "class": styles_input,
            }
        )
    )

    nombre = forms.CharField(
        label="Nombre del catador",
        max_length=50,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$',
                message="El nombre solo puede contener letras y espacios."
            )
        ],
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ej. Mario",
                "class": styles_input,
            }
        )
    )

    apellido = forms.CharField(
        label="Apellido del catador",
        max_length=50,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$',
                message="El apellido solo puede contener letras y espacios."
            )
        ],
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ej. Sánchez",
                "class": styles_input,
            }
        )
    )

    telefono = forms.CharField(
        label="Teléfono",
        max_length=10,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message="El teléfono debe contener solo números (puede incluir + al inicio)."
            )
        ],
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ej. 5512345678",
                "class": styles_input,
                "type": "tel",
            }
        )
    )

    correo = forms.EmailField(
        label="Correo electrónico",
        required=True,
        validators=[EmailValidator(
            message="Introduce un correo electrónico válido.")],
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Ej. mario@example.com",
                "class": styles_input,
            }
        )
    )

    fecha_nacimiento = forms.DateField(
        label="Fecha de nacimiento",
        required=True,
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                "type": "date",
                "class": styles_input,
            }
        ),
        error_messages={
            "invalid": "Introduce una fecha válida (DD-MM-YYYY)."
        }
    )

    GENERO_OPCIONES = [
        ('Hombre', 'Hombre'),
        ('Mujer', 'Mujer')
    ]

    genero = forms.ChoiceField(
        label="Género",
        required=True,
        choices=GENERO_OPCIONES,
        widget=forms.RadioSelect(
            attrs={
                "class": "ct-inputs-pos-cata radio radio-primary checked:bg-cts-secondary mx-2 bg-surface-ligt disabled:bg-cts-fourthy"
            }
        )
    )

    is_update = forms.BooleanField(
        initial=False,
        required=False,
        widget=forms.HiddenInput()
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("nombre_usuario")
        is_update = cleaned_data.get("is_update")

        if not is_update:
            if User.objects.filter(username__iexact=username).exists():
                raise forms.ValidationError(
                    "Este nombre de usuario ya está registrado.")

        return cleaned_data
