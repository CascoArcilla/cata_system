from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from tecnicas.models import SesionSensorial, Catador, Participacion, Producto, Calificacion, Palabra
from controllers import PosicionController, CalificacionController, ParticipacionController, PalabrasController, EscalaController
from .general_test_controller import GenetalTestController


class TestScalesController(GenetalTestController):
    def __init__(self, sensorial_session, user_tester):
        super().__init__(sensorial_session, user_tester)
        self.current_directory = "forms_tester/test_convencional.html"

    def controllGet(self, request: HttpRequest):
        technique = self.session.tecnica
        self.participation = Participacion.objects.get(
            tecnica=technique, catador=request.user.user_catador)

        ctx = self.context
        ctx["session"] = self.session

        # Obtener posiciones y palabras de la técnica
        positions_in_order = PosicionController.getPostionsInOrder(
            id_order=request.session["id_order"])
        aligned_positions_in_order = sorted(
            positions_in_order, key=lambda p: p.posicion)
        words = PalabrasController.getWordsInTechnique(technique=technique)

        # Comprobar siguiente posición sin calificar
        (next_position, end_products) = CalificacionController.checkPositionWithoutRating(
            positions=aligned_positions_in_order,
            user_cata=request.user.user_catador,
            repetition=technique.repeticion,
            technique=technique,
            num_words=len(words)
        )

        # Si no hay productos se finaliza la sesion
        if end_products:
            ParticipacionController.finishSession(self.participation)
            params = {"code_sesion": self.session.codigo_sesion}
            return redirect(reverse('cata_system:catador_init_session', kwargs=params))

        # Si devuelve una lista, tomar el primer elemento
        if isinstance(next_position, list):
            next_position = next_position[0]

        # Producto a calificar ahora
        product = next_position.id_producto
        ctx["product"] = product

        # Revisar las palabras para calificar
        try:
            rating = Calificacion.objects.get(
                num_repeticion=technique.repeticion,
                id_producto=product,
                id_tecnica=technique,
                id_catador=self.tester
            )
            there_rating = True
        except Calificacion.DoesNotExist:
            there_rating = False

        # Si no hay calificaciones previas, usar todas las palabras
        if not there_rating:
            ctx["words"] = words
        else:
            ratings_product = rating.dato_calificacion.all()
            # Filtrar palabras que faltan
            words_to_use = PalabrasController.getWordsWithoutData(
                recoreded_data=ratings_product,
                words=words
            )
            ctx["words"] = words_to_use

        # Escala y etiquetas relacionadas
        scale = EscalaController.getScaleByTechnique(technique=technique)
        ctx["scale"] = scale
        ctx["type_scale"] = scale.id_tipo_escala.nombre_escala
        ctx["tags"] = EscalaController.getRelatedTagsInScale(scale=scale)
        if ctx["type_scale"] == "continua":
            ctx["size_scale"] = {
                "max_size": scale.longitud * 100,
                "middle_size": (scale.longitud * 100)/2
            }

        return render(request, self.current_directory, ctx)
