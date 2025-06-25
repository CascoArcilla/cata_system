from django.db import models

class TipoEscala():
    nombre_escala = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre_escala