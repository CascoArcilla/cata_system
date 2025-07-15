from django.db import models

class CategoriaTecnica(models.Model):
    nombre_categoria = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nombre_categoria