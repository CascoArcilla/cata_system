from django.test import TestCase
from django.urls import reverse
from ..models import Palabra


class TestsApiWords(TestCase):
    def setUp(self):
        Palabra.objects.create(nombre_palabra="salado")

    def test_get_words_fail(self):
        word_name = "dulce"
        expected_error = "no existen palabras"

        response = self.client.get(
            reverse("cata_system:api_palabras")+f"?palabra={word_name}"
        )

        self.assertEqual(response.status_code, 200)

        res_json = response.json()
        self.assertIn("error", res_json)
        self.assertEqual(res_json["error"], expected_error)

    def test_get_words_no_parameter(self):
        expected_error = "parametros no encontrados"

        response = self.client.get(reverse("cata_system:api_palabras"))

        self.assertEqual(response.status_code, 200)

        res_json = response.json()
        self.assertIn("error", res_json)
        self.assertEqual(res_json["error"], expected_error)

    def test_get_words_success(self):
        word_name = "sal"
        expected_message = "datos localizados"

        expected_data = Palabra.objects.filter(nombre_palabra__contains=word_name)

        response = self.client.get(
            reverse("cata_system:api_palabras")+f"?palabra={word_name}"
        )

        self.assertEqual(response.status_code, 200)

        res_json = response.json()

        self.assertIn("message", res_json)
        self.assertEqual(res_json["message"], expected_message)

        data = res_json["data"]
        self.assertEqual(len(data), len(expected_data))

    def test_post_word_success(self):
        word_name = "dulce"
        expected_message = "palabra creada"

        response = self.client.post(
            reverse("cata_system:api_palabras"),
            data={"nombre_palabra": word_name}
        )

        self.assertEqual(response.status_code, 200)

        res_json = response.json()

        self.assertIn("message", res_json)
        self.assertEqual(res_json["message"], expected_message)

        data = res_json["data"]
        self.assertIn("id", data)
        self.assertIn("nombre_palabra", data)
        self.assertEqual(data["nombre_palabra"], word_name)

    def test_post_word_fail(self):
        word_name = "salado"
        expected_error = "palabra repetida"

        response = self.client.post(
            reverse("cata_system:api_palabras"),
            data={"nombre_palabra": word_name}
        )

        self.assertEqual(response.status_code, 200)

        res_json = response.json()
        self.assertIn("error", res_json)
        self.assertEqual(res_json["error"], expected_error)
    
    def test_post_word_no_parameter(self):
        expected_error = "parametros no encontrados"

        response = self.client.post(reverse("cata_system:api_palabras"))

        self.assertEqual(response.status_code, 200)

        res_json = response.json()
        self.assertIn("error", res_json)
        self.assertEqual(res_json["error"], expected_error)