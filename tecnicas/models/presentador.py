from django.contrib.auth.models import User
from django.db import models


class Presentador(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='user_presentador', default=None, null=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    telefono = models.BigIntegerField(default=555)

    def __str__(self):
        return f"Presentador: {self.user.username}"
