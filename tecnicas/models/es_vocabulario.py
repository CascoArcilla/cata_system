from django.db import models

from .tecnica import Tecnica
from .vocabulario import Vocabulario

class EsVocabulario(models.Model):
    id_tecnica = models.OneToOneField(Tecnica, on_delete=models.CASCADE, related_name="tecnica_esvacabulario")
    id_vocabulario = models.ForeignKey(Vocabulario, on_delete=models.CASCADE, related_name="vocabulario_esvocabulario")