from django.db import models
from .calificacion import Calificacion


class DatoPunto(models.Model):
    x = models.FloatField(null=False, default=0)
    y = models.FloatField(null=False, default=0)
    calificacion = models.ForeignKey(
        Calificacion, on_delete=models.CASCADE, related_name="data_punto")

    def __str__(self):
        return f"({self.calificacion.id_producto.codigoProducto}: {self.x}, {self.y})"
