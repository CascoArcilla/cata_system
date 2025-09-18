from django.db import models
from .tecnica import Tecnica
from .catador import Catador


class Participacion(models.Model):
    tecnica = models.ForeignKey(
        Tecnica, on_delete=models.CASCADE, related_name="tecnica_participacion")
    catador = models.ForeignKey(
        Catador, on_delete=models.CASCADE, related_name="catador_participacion")
    activo = models.BooleanField(default=False)
    finalizado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.catador.usuarioCatador} {'activo' if self.activo else 'no activo'}"
