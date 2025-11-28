from django.db import models


class Modalidad(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre
