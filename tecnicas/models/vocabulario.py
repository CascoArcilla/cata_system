from django.db import models
from django.utils import timezone
from .palabra import Palabra


class Vocabulario(models.Model):
    nombre_vocabulario = models.CharField(max_length=255, unique=True)
    descripcion = models.CharField(max_length=255, default="Vocabulario sin descripción")
    palabras = models.ManyToManyField(
        Palabra, related_name="vovabulario_palabras")
    creado = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre_vocabulario
