from django.db import models
from .escala import Escala
from .etiqueta import Etiqueta


class EtiquetasEscala(models.Model):
    id_escala = models.ForeignKey(
        Escala, on_delete=models.CASCADE, related_name="escalas_etiqutas_escala")

    id_etiqueta = models.ForeignKey(
        Etiqueta, on_delete=models.CASCADE, related_name="etiqueta_etiquetas_escala")

    posicion = models.IntegerField()

    def __str__(self):
        return f"Escala {self.id_escala.id}, {self.id_etiqueta.valor_etiqueta}, posicion {self.posicion}"
