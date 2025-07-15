from django.db import models

from .palabra import Palabra

class Vocabulario(models.Model):
    nomre_vocabulario = models.CharField(max_length=255, unique=True)
    palabras = models.ManyToManyField(Palabra, related_name="vovabulario_palabras")

    def __str__(self):
        return self.nomre_vocabulario