from django.db import models

class Presentador(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    nombre_usuario = models.CharField(max_length=255)
    contrasena = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre
