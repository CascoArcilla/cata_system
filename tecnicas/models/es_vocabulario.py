from django.db import models

from .estilo_palabra import EstiloPalabra
from .vocabulario import Vocabulario

class EsVocabulario(models.Model):
    id_estilo = models.ForeignKey(EstiloPalabra, on_delete=models.CASCADE, related_name="estilo_esvacabulario")
    id_vocabulario = models.ForeignKey(Vocabulario, on_delete=models.CASCADE, related_name="vocabulario_esvocabulario")