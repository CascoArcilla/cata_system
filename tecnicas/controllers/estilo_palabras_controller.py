from ..models import EsAtributo, Tecnica, Palabra
from django.db import DatabaseError
from ..utils import controller_error


class EstiloPalabrasController():
    def __init__(self, technique: Tecnica = None, words: list[Palabra] = None):
        self.technique = technique
        self.list_words = words

    def setTechnique(self, technique: Tecnica):
        self.technique = technique

    def setListWords(self, new_words: list[Palabra]):
        self.list_words = new_words

    def createAndSaveInstaceStyle(self):
        try:
            self.instanceStyle = EsAtributo.objects.create(
                id_tecnica=self.technique)
            return self.instanceStyle
        except DatabaseError as error:
            return controller_error("error al registrar el estilo con tecnica")

    def relatedWords(self):
        if not self.list_words:
            return controller_error("no existen palabras para asociar")
        try:
            self.instanceStyle.palabras.add(*self.list_words)
            return self.instanceStyle.palabras
        except DatabaseError as error:
            return controller_error("error al relacionar palabras con el estilo tecnica")
