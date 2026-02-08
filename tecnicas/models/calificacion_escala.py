from django.db import models
from .calificacion import Calificacion
from .escala import Escala


class CalificacionEscala(models.Model):
    calificacion = models.ForeignKey(Calificacion, on_delete=models.CASCADE, related_name="calificacion_escala")
    escala = models.ForeignKey(Escala, on_delete=models.CASCADE, related_name="calificacion_escala")

    class Meta:
        db_table = 'calificacion_escala'
        verbose_name = 'Calificación Escala'
        verbose_name_plural = 'Calificaciones Escalas'
        unique_together = ('calificacion', 'escala')

    def __str__(self):
        return f'{self.calificacion.id_tecnica.sesion_tecnica.codigo_sesion} - {self.calificacion.num_repeticion} repeticion - {self.calificacion.id_producto.codigoProducto} - {self.escala.id_tipo_escala.nombre_escala} - {self.calificacion.id_catador.user.username}'
