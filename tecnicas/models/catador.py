from django.db import models

class Catador():
    usuarioCatador = models.CharField(max_length=255, unique=True)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    telefono = models.BigIntegerField()
    correo = models.EmailField()