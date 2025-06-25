from django.db import models

from .palabra import Palabra
from .es_atributo import EsAtributo

class ListaPalabra(models.Model):
    id_palabra = models.ForeignKey(Palabra, on_delete=models.CASCADE, related_name="palabra_listapalabras")
    id_atributos = models.ForeignKey(EsAtributo, on_delete=models.CASCADE, related_name="atributo_listapalabras")
