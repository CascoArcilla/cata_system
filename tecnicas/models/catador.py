from django.contrib.auth.models import User
from django.db import models


class Catador(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='user_catador', default=None, null=True)
    nacimiento = models.DateField(null=True, blank=True)
    telefono = models.BigIntegerField(default=555)
    genero = models.CharField(
        max_length=10,
        choices=[('Hombre', 'Hombre'), ('Mujer', 'Mujer')],
        null=True, blank=True, default="Hombre"
    )

    def __str__(self):
        return f"Catador: {self.user.username}"
