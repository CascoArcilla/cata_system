from django.test import TestCase
from django.urls import reverse
from ..controllers import PalabrasController
from ..models import Palabra


class TestsApiWords(TestCase):
    ids: list[int]
    words_saved: list[Palabra]

    def setUp(self):
        self.named_words = ["rasposo", "afilado", "poroso"]
        words_to_save = [Palabra(nombre_palabra=name)
                         for name in self.named_words]
        self.words_saved = Palabra.objects.bulk_create(words_to_save)
        self.ids = [word.id for word in self.words_saved]

    def test_get_words_by_list_ids(self):
        instance = PalabrasController(ids=self.ids)
        new_words = Palabra.objects.filter(id__in=self.ids)
        names = [word.nombre_palabra for word in new_words]
        self.assertEqual(set(self.named_words), set(names))

    def test_get_words_by_list_ids_fail(self):
        instance = PalabrasController(ids=[23, 12, 76])
        response = instance.setWords()
        self.assertIn("error", response)
