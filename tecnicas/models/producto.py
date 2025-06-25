from django.db import models

from .sesion_sensorial import SesionSensorial

class Producto(models.Model):
    codigoProducto = models.CharField(max_length=3)
    id_sesion = models.ForeignKey(SesionSensorial, on_delete=models.CASCADE, related_name="productos_sesion")

    def __str__(self):
        return self.codigoProducto