from django.db import models
from .tecnica import Tecnica
from .modalidad import Modalidad


class TecnicaModalidad(models.Model):
    tecnica = models.ForeignKey(
        Tecnica, on_delete=models.CASCADE, related_name="tecnica_modalidad")
    modalidad = models.ForeignKey(
        Modalidad, on_delete=models.CASCADE, related_name="modalidad_tecnica")

    usando = models.BooleanField(default=False)
