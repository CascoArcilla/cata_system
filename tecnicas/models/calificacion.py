from django.db import models

from .producto import Producto
from .tecnica import Tecnica
from .catador import Catador

class Calificacion(models.Model):
    num_repeticion = models.IntegerField()
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="calificacion_producto")
    id_tecnica = models.ForeignKey(Tecnica, on_delete=models.CASCADE, related_name="calificacion_tecnica")
    id_catador = models.ForeignKey(Catador, on_delete=models.CASCADE, related_name="calificacion_catador")

    def __str__(self):
        return f"{self.id} - {self.id_tecnica.sesion_tecnica} - {self.num_repeticion} - {self.id_catador.user.username}"