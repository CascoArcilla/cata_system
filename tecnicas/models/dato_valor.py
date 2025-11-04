from django.db import models

from .dato import Dato


class ValorDecimal(models.Model):
    id_dato = models.OneToOneField(
        Dato, on_delete=models.CASCADE, related_name="dato_decimal")
    valor = models.FloatField()

    def __str__(self):
        return f"{self.id} - {self.id_dato.id_palabra}: {self.valor} - {self.id_dato.id_calificacion.id_catador.user.username}"


class ValorBooleano(models.Model):
    id_dato = models.OneToOneField(
        Dato, on_delete=models.CASCADE, related_name="dato_boolean")
    valor = models.BooleanField()

    def __str__(self):
        return f"{self.id} - {self.id_dato.id_palabra}: {self.valor} - {self.id_dato.id_calificacion.id_catador.user.username}"
