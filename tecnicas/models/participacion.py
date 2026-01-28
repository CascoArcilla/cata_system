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
    last_activity = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.catador.user.username} {'activo' if self.activo else 'no activo'} - {self.tecnica.sesion_tecnica.nombre_sesion}"
