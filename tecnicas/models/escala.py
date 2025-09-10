from django.db import models

from .tipo_escala import TipoEscala
from .tecnica import Tecnica

class Escala(models.Model):
    id_tipo_escala = models.ForeignKey(TipoEscala, on_delete=models.CASCADE, related_name="escala_tipo_escala")
    longitud = models.IntegerField()
    tecnica = models.OneToOneField(Tecnica, on_delete=models.CASCADE, related_name="escala_tecnica")

    def __str__(self):
        return self.id_tipo_escala.nombre_escala