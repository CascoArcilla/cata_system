from django.db import models

from .estilo_palabra import EstiloPalabra

class Tecnica(models.Model):
    nombre_tecnica = models.CharField(max_length=255)
    maximas_repeticiones = models.IntegerField(default=0)
    repecion = models.IntegerField(default=0)
    limite_catadores = models.IntegerField()
    instrucciones = models.CharField(max_length=255)
    id_estilo = models.ForeignKey(EstiloPalabra, on_delete=models.CASCADE, related_name="estilo_tecnica")

    def __str__(self):
        return self.nombre_tecnica