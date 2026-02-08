from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from tecnicas.models import Participacion, Producto, Calificacion, Escala
from tecnicas.controllers import InitSessionPerfilIdealController, ParticipacionController, EscalaController
from .general_test_controller import GenetalTestController
from tecnicas.controllers import PalabrasController
import random


class TestPerfilIdealPhase2Controller(GenetalTestController):
    def __init__(self, sensorial_session, user_tester):
        super().__init__(sensorial_session, user_tester)
        self.current_directory = "tecnicas/forms_tester/test_perfil_ideal_phase2.html"

    def controllGet(self, request: HttpRequest):
        technique = self.session.tecnica
        self.participation = Participacion.objects.get(
            tecnica=technique, catador=request.user.user_catador)

        self.context["session"] = self.session

        products_in_technique = Producto.objects.filter(id_tecnica=technique)

        # Comprobar si la Fase 1 está completa
        num_words = len(
            PalabrasController.getWordsInTechnique(technique=technique))

        end_phase1 = InitSessionPerfilIdealController.endPhase1(num_products=len(
            products_in_technique), num_words=num_words, participation=self.participation)

        if not end_phase1[0]:
            # Si la Fase 1 no está completa, redirigir a Fase 1
            params = {"code_sesion": self.session.codigo_sesion}
            return redirect(reverse("cata_system:session_perfil_ideal_phase1", kwargs=params))

        # Obtener la escala hedónica
        hedonic_scale = Escala.objects.select_related("id_tipo_escala").get(
            tecnica=technique,
            id_tipo_escala__nombre_escala="hedonica"
        )

        # Obtener todas las calificaciones de la Fase 2
        ratings = Calificacion.objects.filter(
            num_repeticion=technique.repeticion,
            id_tecnica=technique,
            id_catador=self.tester,
            id_producto__in=products_in_technique,
            calificacion_escala__escala=hedonic_scale
        ).select_related(
            'id_producto'
        ).prefetch_related("dato_hedonico")

        # Crear diccionario para acceso rápido a calificaciones por producto
        ratings_dict = {}
        try:
            for rating in ratings:
                ratings_dict[rating.id_producto.id] = rating
        except Exception as e:
            print(f"Error generando diccionario de calificaciones: {e}")
            ratings_dict = {}

        # Buscar productos sin calificación hedónica
        products_pending = []

        for current_product in products_in_technique:
            id_product = current_product.id
            rating_hedonic = ratings_dict.get(id_product)
            if not rating_hedonic:
                products_pending.append(current_product)

        # Si no hay productos pendientes, finalizar participación
        if not products_pending:
            ParticipacionController.finishSession(self.participation)
            params = {"code_sesion": self.session.codigo_sesion}
            return redirect(reverse(self.previus_directory, kwargs=params))

        # Seleccionar producto aleatoriamente de los pendientes
        use_product = random.choice(products_pending)

        self.context["product"] = use_product
        self.context["hedonic_scale"] = hedonic_scale

        # Obtener etiquetas de la escala hedónica
        hedonic_tags = EscalaController.getRelatedTagsInScale(
            scale=hedonic_scale)
        print(hedonic_tags)

        self.context["tags"] = hedonic_tags

        return render(request, self.current_directory, self.context)
