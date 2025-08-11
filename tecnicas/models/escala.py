from django.db import models

from .tipo_escala import TipoEscala

class Escala(models.Model):
    id_tipo_escala = models.ForeignKey(TipoEscala, on_delete=models.CASCADE, related_name="escala_tipo_escala")
    longitud = models.IntegerField()

    def __str__(self):
        return self.longitud