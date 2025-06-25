from django.db import models

from .presentador import Presentador
from .tecnica import Tecnica

class SesionSensorial(models.Model):
    fechaCreacion = models.DateTimeField("date published")
    activo = models.BooleanField(default=False)
    creadoPor = models.ForeignKey(Presentador, on_delete=models.CASCADE, related_name="presentador_sesion")
    tecnica = models.ForeignKey(Tecnica, on_delete=models.CASCADE, related_name="sesion_tecnica")