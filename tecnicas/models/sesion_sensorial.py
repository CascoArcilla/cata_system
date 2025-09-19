from django.db import models
from django.utils import timezone
from .presentador import Presentador
from .tecnica import Tecnica
import shortuuid


class SesionSensorial(models.Model):
    codigo_sesion = models.CharField(
        primary_key=True, default=shortuuid.uuid, editable=False, max_length=22)
    nombre_sesion = models.CharField(max_length=255, null=True)
    fechaCreacion = models.DateTimeField(default=timezone.now)
    activo = models.BooleanField(default=False)
    creadoPor = models.ForeignKey(
        Presentador, on_delete=models.CASCADE, related_name="presentador_sesion")
    tecnica = models.OneToOneField(
        Tecnica, on_delete=models.CASCADE, related_name="sesion_tecnica")

    def __str__(self):
        return self.nombre_sesion if self.nombre_sesion else self.codigo_sesion
