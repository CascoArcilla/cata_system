from django.db import models

from .escala import Escala
from .etiqueta import Etiqueta

class EtiquetasEscala(models.Model):
    id_escala = models.ForeignKey(Escala, on_delete=models.CASCADE, related_name="escalas_etiqutas_escala")
    id_etiqueta = models.ForeignKey(Etiqueta, on_delete=models.CASCADE, related_name="etiqueta_etiquetas_escala")
    posicion = models.IntegerField()