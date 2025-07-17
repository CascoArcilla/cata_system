from django.db import models

from .categoria_tecnica import CategoriaTecnica

class TipoTecnica(models.Model):
    nombre_tecnica = models.CharField(max_length=255, unique=True)
    id_categoria_tecnica = models.ForeignKey(CategoriaTecnica, on_delete=models.CASCADE, related_name="tipo_tecnica_categoria_tecnica")

    def __str__(self):
        return self.nombre_tecnica