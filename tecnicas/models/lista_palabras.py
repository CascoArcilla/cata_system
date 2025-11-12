from django.db import models
from tecnicas.models import Tecnica, Catador, Palabra


class ListaPalabras(models.Model):
    tecnica = models.ForeignKey(
        Tecnica, on_delete=models.CASCADE, related_name="tecnica_lista")
    catador = models.ForeignKey(
        Catador, on_delete=models.CASCADE, related_name="catador_lista")
    es_final = models.BooleanField(default=False)
    palabras = models.ManyToManyField(
        Palabra, related_name="lista_palabras")

    def __str__(self):
        return f"{self.tecnica.codigo_sesion} - {self.catador.user.username}"
