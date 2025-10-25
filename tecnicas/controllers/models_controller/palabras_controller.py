from ...models import Palabra, Tecnica, EsAtributo, EsVocabulario, Dato
from django.db import DatabaseError
from ...utils import controller_error


class PalabrasController():
    ids_words: list[int]
    words: list[Palabra]

    def __init__(self, ids: list[int]):
        self.ids_words = ids

    def setIdsWords(self, new_ids: list[int]):
        self.ids_words = new_ids

    def setWords(self):
        self.words = []
        searched_words = list(Palabra.objects.filter(id__in=self.ids_words))
        if not len(searched_words):
            return controller_error("No se han encontrado registros")
        self.words = searched_words
        return self.words

    @staticmethod
    def getWordsInTechnique(technique: Tecnica):
        if technique.id_estilo.nombre_estilo == "atributos":
            es_atribute = EsAtributo.objects.get(id_tecnica=technique)
            words = list(es_atribute.palabras.all())
            return words
        elif technique.id_estilo.nombre_estilo == "vocabulario":
            try:
                palabras = Palabra.objects.filter(
                    vocabulario__esvocabulario__id_tecnica=technique
                )
                return list(palabras.distinct()) if palabras.exists() else controller_error("Técnica sin palabras con vocabulario")
            except Exception as e:
                return controller_error("Técnica sin palabras con vocabulario")

    @staticmethod
    def getWordsWithoutData(recoreded_data: list[Dato], words: list[Palabra]):
        qualified_words = [data.id_palabra for data in recoreded_data]

        if set(qualified_words) == set(words):
            return controller_error("No hay palabras por usar")

        words_without_use = list(set(words).difference(set(qualified_words)))

        return words_without_use
