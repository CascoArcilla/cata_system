from django.db import models

from .estilo_palabra import EstiloPalabra
from .tipo_tecnica import TipoTecnica


class Tecnica(models.Model):
    tipo_tecnica = models.ForeignKey(
        TipoTecnica, on_delete=models.CASCADE, related_name="tecnica_tipo_tecnica")
    repeticiones_max = models.IntegerField(default=0)
    repecion = models.IntegerField(default=0)
    limite_catadores = models.IntegerField()
    instrucciones = models.CharField(max_length=255)
    id_estilo = models.ForeignKey(
        EstiloPalabra, on_delete=models.CASCADE, related_name="estilo_tecnica")

    def __str__(self):
        return self.tipo_tecnica.nombre_tecnica

    def toDict(self):
        return {
            "tipo_tecnica": self.tipo_tecnica,
            "repeticiones_max": self.repeticiones_max,
            "repecion": self.repecion,
            "limite_catadores": self.limite_catadores,
            "instrucciones": self.instrucciones,
            "id_estilo": self.id_estilo,
        }
