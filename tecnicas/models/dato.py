from django.db import models

from .palabra import Palabra
from .calificacion import Calificacion


class Dato(models.Model):
    id_palabra = models.ForeignKey(
        Palabra, on_delete=models.CASCADE, related_name="dato_palabra")
    id_calificacion = models.ForeignKey(
        Calificacion, on_delete=models.CASCADE, related_name="dato_calificacion")

    def __str__(self):
        return f"{self.id_palabra.nombre_palabra} - {self.id_calificacion.id_producto.codigoProducto}"
