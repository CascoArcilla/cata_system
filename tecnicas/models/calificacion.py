from django.db import models

from .producto import Producto
from .tecnica_intensidad import TecnicaIntensidad
from .catador import Catador

class Calificacion(models.Model):
    num_repeticion = models.IntegerField()
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="calificacion_producto")
    id_intensidad = models.ForeignKey(TecnicaIntensidad, on_delete=models.CASCADE, related_name="calificacion_tec_intensidad")
    id_catador = models.ForeignKey(Catador, on_delete=models.CASCADE, related_name="calificacion_catador")