from django.db import models

from .escala import Escala
from .tecnica import Tecnica

class TecnicaIntensidad(models.Model):
    id_tecnica = models.OneToOneField(Tecnica, on_delete=models.CASCADE, related_name="tecnica_intensidad")
    id_escala = models.OneToOneField(Escala, on_delete=models.CASCADE, related_name="escala_intensidad")