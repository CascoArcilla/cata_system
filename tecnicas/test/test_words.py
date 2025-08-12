from django.test import TestCase
from django.urls import reverse
from ..models import Palabra


class TestsApiWords(TestCase):
    def setUp(self):
        Palabra.objects.create(nombre_palabra="salado")

    def test_get_word_fail(self):
        word_name = "dulce"
        expected_error = "palabra no encontrada"

        response = self.client.get(
            reverse("cata_system:api_palabras")+f"?palabra={word_name}"
        )

        self.assertEqual(response.status_code, 200)

        res_json = response.json()
        self.assertIn("error", res_json)
        self.assertEqual(res_json["error"], expected_error)

    def test_get_word_no_parameter(self):
        expected_error = "parametros no encontrados"

        response = self.client.get(reverse("cata_system:api_palabras"))

        self.assertEqual(response.status_code, 200)

        res_json = response.json()
        self.assertIn("error", res_json)
        self.assertEqual(res_json["error"], expected_error)

    def test_get_word_success(self):
        word_name = "salado"
        expected_message = "dato localizado"

        expected_data = Palabra.objects.get(nombre_palabra=word_name).to_dict()

        response = self.client.get(
            reverse("cata_system:api_palabras")+f"?palabra={word_name}"
        )

        self.assertEqual(response.status_code, 200)

        res_json = response.json()

        self.assertIn("message", res_json)
        self.assertEqual(res_json["message"], expected_message)

        data = res_json["data"]
        self.assertEqual(data["id"], expected_data["id"])
        self.assertEqual(data["name"], expected_data["nombre_palabra"])
