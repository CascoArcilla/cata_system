from django.db import models

from .tecnica import Tecnica
from .catador import Catador
from .producto import Producto

class Orden(models.Model):
    id_tecnica = models.ForeignKey(Tecnica, on_delete=models.CASCADE, related_name="orden_tecnica")
    id_catador = models.ForeignKey(Catador, on_delete=models.CASCADE, related_name="orden_catador")

class Posicion(models.Model):
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="posicion_producto")
    id_orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name="posicion_orden")
    posicion = models.IntegerField()