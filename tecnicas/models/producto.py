from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .tecnica import Tecnica
from cloudinary.models import CloudinaryField
from django.core.exceptions import ValidationError
from utils import delete_images


def validate_file_size(value):
    limit = 2 * 1024 * 1024  # 2MB
    if value.size > limit:
        raise ValidationError(
            'El archivo es demasiado grande. El límite es 2MB.')


class Producto(models.Model):
    codigoProducto = models.CharField(max_length=3)
    id_tecnica = models.ForeignKey(
        Tecnica, on_delete=models.CASCADE, related_name="producto_tecnica")
    imagen = CloudinaryField(
        'imagen',
        folder='cata_system/uploads/',
        null=True,
        blank=True,
        transformation={
            'quality': 'auto',
            'fetch_format': 'auto',
            'width': 1000,
            'crop': 'limit'
        }
    )

    def __str__(self):
        return self.codigoProducto


@receiver(post_delete, sender=Producto)
def eliminar_imagen_cloudinary(sender, instance, **kwargs):
    if instance.imagen:
        # Obtenemos el public_id, ya sea del objeto CloudinaryResource o del string
        public_id = getattr(instance.imagen, 'public_id', str(instance.imagen))
        if public_id:
            delete_images([public_id])
