from django.db import models
from tecnicas.models import Tecnica, Catador, Palabra, Producto


class GrupoProducto(models.Model):
    tecnica = models.ForeignKey(
        Tecnica, on_delete=models.CASCADE, related_name="tecnica_grupo_producto")
    
    catador = models.ForeignKey(
        Catador, on_delete=models.CASCADE, related_name="catador_grupo_producto")

    productos = models.ManyToManyField(
        Producto, related_name="grupo_producto")

    palabras = models.ManyToManyField(
        Palabra, related_name="grupo_producto")

    def __str__(self):
        return f"{self.tecnica.sesion_tecnica.codigo_sesion} - {self.catador.user.username}"
