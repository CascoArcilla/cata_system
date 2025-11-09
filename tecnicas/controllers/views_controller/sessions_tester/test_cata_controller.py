from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from tecnicas.models import Producto, Participacion, Palabra, Calificacion
from tecnicas.controllers import PalabrasController
from .general_test_controller import GenetalTestController


class TestCataController(GenetalTestController):
    def __init__(self, sensorial_session, user_tester):
        super().__init__(sensorial_session, user_tester)
        self.current_directory = "tecnicas/forms_tester/cata.html"

    def controllGet(self, request: HttpRequest):
        technique = self.session.tecnica
        self.participation = Participacion.objects.get(
            tecnica=technique, catador=request.user.user_catador)

        self.context["session"] = self.session

        products_in_technique = Producto.objects.filter(id_tecnica=technique)

        words = PalabrasController.getWordsInTechnique(technique=technique)

        use_product: Producto = None
        use_words: list[Palabra] = None

        # Revisamos el producto que le falten calificaciones
        for current_product in products_in_technique:
            try:
                rating = Calificacion.objects.get(
                    num_repeticion=technique.repeticion,
                    id_producto=current_product,
                    id_tecnica=technique,
                    id_catador=self.tester
                )
            except Calificacion.DoesNotExist:
                # Si no hay calificacion mandamos el producto actual y todas la palabras
                use_product = current_product
                use_words = words
                break

        # Si no hay producto que falta por calificar finalizar sesion para el Catador
        if not use_product:
            updated_participation = ParticipacionController.finishSession(
                self.participation)
            params = {
                "code_sesion": self.session.codigo_sesion
            }
            return redirect(reverse(self.previus_directory, kwargs=params))

        self.context["product"] = use_product
        self.context["words"] = use_words

        return render(request, self.current_directory, self.context)
