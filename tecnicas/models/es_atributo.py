from django.db import models

from .estilo_palabra import EstiloPalabra

class EsAtributo(models.Model):
    id_estilo = models.ForeignKey(EstiloPalabra, on_delete=models.CASCADE, related_name="estilo_esatributo")