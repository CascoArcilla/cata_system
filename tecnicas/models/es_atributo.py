from django.db import models

from .tecnica import Tecnica
from .palabra import Palabra

class EsAtributo(models.Model):
    id_tecnica = models.OneToOneField(Tecnica, on_delete=models.CASCADE, related_name="tecnica_esatributo")
    palabras = models.ManyToManyField(Palabra, related_name="estilo_atributo_palabras")