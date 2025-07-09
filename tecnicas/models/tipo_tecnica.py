from django.db import models

class TipoTecnica(models.Model):
    nombre_tecnica = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre_tecnica