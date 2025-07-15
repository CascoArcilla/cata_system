from django.db import models

class Catador(models.Model):
    usuarioCatador = models.CharField(max_length=255, unique=True)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    telefono = models.BigIntegerField()
    correo = models.EmailField()
    fechaNacimiento = models.DateField()

    def __str__(self):
        return self.usuarioCatador