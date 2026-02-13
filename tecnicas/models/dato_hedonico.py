from django.db import models
from .calificacion import Calificacion


class DatoHedonico(models.Model):
    calificacion = models.ForeignKey(Calificacion, on_delete=models.CASCADE, related_name="dato_hedonico")
    valor = models.IntegerField()

    def __str__(self):
        return f"{self.calificacion.id_tecnica.nombre_tecnica} - {self.calificacion.id_producto.codigoProducto} - {self.calificacion.id_catador.user.username} - {self.valor}"
