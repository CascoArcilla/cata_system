from django import forms
from PIL import Image


class ImagesProductForm(forms.Form):
    def __init__(self, *args, codes: list = [], **kwargs):
        super().__init__(*args, **kwargs)

        for code in codes:
            self.fields[f'imagen_{code}'] = forms.ImageField(
                required=False,
                label=f"Producto {code}",
                help_text="Imagen opcional, max 2MB",
                widget=forms.FileInput(attrs={
                    "class": "text-sm text-center px-2 py-1 rounded text-white border-black bg-cts-fifthy w-full cursor-pointer btn-push",
                    "accept": "image/*"
                })
            )

    def clean(self):
        cleaned_data = super().clean()

        for field_name, value in cleaned_data.items():
            if field_name.startswith('imagen_') and value:
                # Validate image size (max 2MB)
                if value.size > 2 * 1024 * 1024:
                    raise forms.ValidationError(
                        f"La imagen {field_name} es demasiado grande. El límite es 2MB.")

                # Validate if it is really an image
                try:
                    img = Image.open(value)
                    img.verify()
                except Exception:
                    raise forms.ValidationError(
                        f"El archivo subido para {field_name} no es una imagen válida o está corrupto."
                    )
                finally:
                    if hasattr(value, 'seek'):
                        value.seek(0)
                    elif hasattr(value, 'file') and hasattr(value.file, 'seek'):
                        value.file.seek(0)

        return cleaned_data
