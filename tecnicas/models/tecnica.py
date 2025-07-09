from django.db import models

from .estilo_palabra import EstiloPalabra
from .tipo_tecnica import TipoTecnica

class Tecnica(models.Model):
    tipo_tecnica = models.ForeignKey(TipoTecnica, on_delete=models.CASCADE, related_name="tecnica_tipo_tecnica")
    maximas_repeticiones = models.IntegerField(default=0)
    repecion = models.IntegerField(default=0)
    limite_catadores = models.IntegerField()
    instrucciones = models.CharField(max_length=255)
    id_estilo = models.ForeignKey(EstiloPalabra, on_delete=models.CASCADE, related_name="estilo_tecnica")

    def __str__(self):
        return self.tipo_tecnica