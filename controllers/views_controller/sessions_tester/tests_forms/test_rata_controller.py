from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from tecnicas.models import Participacion, Producto, Calificacion, Palabra
from controllers import ParticipacionController, PalabrasController, EscalaController
from .general_test_controller import GenetalTestController


class TestRataController(GenetalTestController):
    def __init__(self, sensorial_session, user_tester):
        super().__init__(sensorial_session, user_tester)
        self.current_directory = "tecnicas/forms_tester/test_convencional.html"

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

            # Obtener los datos asociados para la calificacion para ver que palabras quedan por calificar
            recoreded_data = rating.dato_calificacion.all()

            if not recoreded_data:
                # Si no hay datos entonces devolver el producto con todas las palabras
                use_product = current_product
                use_words = words
                break
            else:
                words_to_use = PalabrasController.getWordsWithoutData(
                    recoreded_data=recoreded_data, words=words)

                # Si quedan palabras por calificar mandar las palabras con el producto
                if not isinstance(words_to_use, dict) and words_to_use:
                    use_product = current_product
                    use_words = words_to_use
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

        # Agregar informacion de la escala
        scale = EscalaController.getScaleByTechnique(technique=technique)
        self.context["scale"] = scale
        self.context["type_scale"] = scale.id_tipo_escala.nombre_escala

        use_tags = EscalaController.getRelatedTagsInScale(scale=scale)
        self.context["tags"] = use_tags
        
        if self.context["type_scale"] == "continua":
            self.context["size_scale"] = {
                "max_size": scale.longitud * 100,
                "middle_size": (scale.longitud * 100)/2
            }

        return render(request, self.current_directory, self.context)
