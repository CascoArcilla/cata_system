from django.db import models

from .etiqueta import Etiqueta
from .tipo_escala import TipoEscala

class Escala(models.Model):
    id_tipo_escala = models.ForeignKey(TipoEscala, on_delete=models.CASCADE, related_name="escala_tipo_escala")
    longitud = models.IntegerField()
    etiquetas = models.ManyToManyField(Etiqueta)

    def __str__(self):
        return self.longitud