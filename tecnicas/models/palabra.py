from django.db import models

class Palabra(models.Model):
    nombre_palabra = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.nombre_palabra