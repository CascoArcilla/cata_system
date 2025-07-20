from django.db import models

from .tecnica import Tecnica

class Producto(models.Model):
    codigoProducto = models.CharField(max_length=3)
    id_tecnica = models.ForeignKey(Tecnica, on_delete=models.CASCADE, related_name="producto_tecnica")

    def __str__(self):
        return self.codigoProducto