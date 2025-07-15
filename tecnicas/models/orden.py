from django.db import models

from .tecnica_intensidad import TecnicaIntensidad
from .catador import Catador
from .producto import Producto

class Orden(models.Model):
    id_intensidad = models.ForeignKey(TecnicaIntensidad, on_delete=models.CASCADE, related_name="orden_tecnica_intensidad")
    id_catador = models.ForeignKey(Catador, on_delete=models.CASCADE, related_name="orden_catador")

class Posicion(models.Model):
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="posicion_producto")
    id_orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name="posicion_orden")
    posicion = models.IntegerField(max_length=2)