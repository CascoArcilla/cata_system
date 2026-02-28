from tecnicas.models import Palabra, Tecnica, EsAtributo, EsVocabulario, Dato
from django.db import DatabaseError
from utils import controller_error


class PalabrasController():
    ids_words: list[int]
    words: list[Palabra]

    def __init__(self, ids: list[int]):
        self.ids_words = ids

    def setIdsWords(self, new_ids: list[int]):
        self.ids_words = new_ids

    def setWords(self):
        self.words = list(Palabra.objects.filter(id__in=self.ids_words))
        if not len(self.words):
            return controller_error("No se han encontrado registros")
        return self.words

    @staticmethod
    def getWordsInTechnique(technique: Tecnica):
        if technique.id_estilo.nombre_estilo == "atributos":
            words = list(technique.tecnica_esatributo.palabras.all())
            if not words:
                return controller_error("Técnica sin palabras")
            return words
        elif technique.id_estilo.nombre_estilo == "vocabulario":
            words = list(
                technique.tecnica_esvacabulario.id_vocabulario.palabras.all())
            if not words:
                return controller_error("Técnica sin palabras con vocabulario")
            return words

    @staticmethod
    def getWordsWithoutData(recoreded_data: list[Dato], words: list[Palabra]):
        qualified_words = [data.id_palabra for data in recoreded_data]

        if set(qualified_words) == set(words):
            return controller_error("No hay palabras por usar")

        words_without_use = list(set(words).difference(set(qualified_words)))

        return words_without_use
