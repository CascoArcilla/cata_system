from django.db import models

from .escala import Escala

class TecnicaIntensidad(models.Model):
    id_escala = models.ForeignKey(Escala)