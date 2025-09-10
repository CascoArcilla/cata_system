from ..models import Palabra
from django.db import DatabaseError
from ..utils import controller_error


class PalabrasController():
    ids_words: list[int]
    words: list[Palabra]

    def __init__(self, ids: list[int]):
        self.ids_words = ids

    def setIdsWords(self, new_ids: list[int]):
        self.ids_words = new_ids

    def setWords(self):
        self.words = []
        try:
            searched_words = Palabra.objects.filter(id__in=self.ids_words)
            if not len(searched_words):
                return controller_error("no se han encontrado registros")
            self.words = searched_words
            return self.words
        except DatabaseError as error:
            return controller_error("error al guardar buscar palabras")
