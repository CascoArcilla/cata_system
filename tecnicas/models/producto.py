from django.db import models

from .tecnica_intensidad import TecnicaIntensidad

class Producto(models.Model):
    codigoProducto = models.CharField(max_length=3)
    id_intensidad = models.ForeignKey(TecnicaIntensidad, on_delete=models.CASCADE, related_name="producto_tecnica_intensidad")

    def __str__(self):
        return self.codigoProducto