from django.db import models

class Etiqueta(models.Model):
    valor_etiqueta = models.CharField(max_length=255)

    def __str__(self):
        return self.valor_etiqueta