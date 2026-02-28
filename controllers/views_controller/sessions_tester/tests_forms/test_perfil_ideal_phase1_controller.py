from django.http import HttpRequest, JsonResponse
from django.db.models import Q, Prefetch
from django.shortcuts import redirect, render
from django.urls import reverse
from tecnicas.models import Participacion, Producto, Calificacion, Palabra, Escala, Dato
from controllers import InitSessionPerfilIdealController, ParticipacionController, PalabrasController, EscalaController
from .general_test_controller import GenetalTestController
import random


class TestPerfilIdealPhase1Controller(GenetalTestController):
    def __init__(self, sensorial_session, user_tester):
        super().__init__(sensorial_session, user_tester)
        self.current_directory = "forms_tester/test_perfil_ideal_phase1.html"

    def controllGet(self, request: HttpRequest):
        technique = self.session.tecnica
        self.participation = Participacion.objects.get(
            tecnica=technique, catador=request.user.user_catador)

        self.context["session"] = self.session

        products_in_technique = Producto.objects.filter(id_tecnica=technique)
        words = PalabrasController.getWordsInTechnique(technique=technique)

        end_phase1 = InitSessionPerfilIdealController.endPhase1(num_products=len(products_in_technique), num_words=len(words), participation=self.participation)

        if end_phase1[0]:
            params = {"code_sesion": self.session.codigo_sesion}
            return redirect(reverse("cata_system:session_perfil_ideal_phase2", kwargs=params))

        # Obtener las escalas con una sola consulta usando Q objects
        scales = Escala.objects.select_related("id_tipo_escala").filter(
            tecnica=technique,
            id_tipo_escala__nombre_escala__in=["estructurada", "ideal"]
        ).order_by('id_tipo_escala__nombre_escala')

        # Mapear escalas por tipo para acceso rápido
        scales_by_type = {
            scale.id_tipo_escala.nombre_escala: scale for scale in scales}

        # Prefetch todas las calificaciones y datos relacionados en una sola consulta
        # Crear un prefetch para los datos de calificación
        data_prefetch = Prefetch(
            'dato_calificacion',
            queryset=Dato.objects.select_related(
                'id_palabra')
        )

        # Obtener todas las calificaciones relevantes en una sola consulta
        ratings = Calificacion.objects.filter(
            num_repeticion=technique.repeticion,
            id_tecnica=technique,
            id_catador=self.tester,
            id_producto__in=products_in_technique,
            calificacion_escala__escala=scales_by_type.get("estructurada")
        ).select_related(
            'id_producto'
        ).prefetch_related(data_prefetch, 'calificacion_escala')

        # Crear diccionario para acceso rápido a calificaciones por producto
        ratings_dict = {}
        try:
            for rating in ratings:
                product_id = rating.id_producto.id
                if product_id not in ratings_dict:
                    ratings_dict[product_id] = {}
                
                # Iterar sobre las escalas relacionadas
                for cal_escala in rating.calificacion_escala.all():
                    ratings_dict[product_id][cal_escala.escala_id] = rating
        except Exception as e:
            print(f"Error generando diccionario de calificaciones: {e}")
            ratings_dict = {}

        # Procesar productos
        products_pending = []
        use_product = None

        for current_product in products_in_technique:
            product_id = current_product.id

            # Verificar si existe calificación de intensidad para este producto
            intensity_scale_id = scales_by_type.get(
                "estructurada").id if "estructurada" in scales_by_type else None

            if not intensity_scale_id or product_id not in ratings_dict:
                products_pending.append(current_product)
                continue

            # Obtener calificación de intensidad desde el diccionario
            rating_intensity = ratings_dict[product_id].get(
                intensity_scale_id)

            if not rating_intensity:
                products_pending.append(current_product)
                continue

            # Verificar si las palabras tiene su dato
            recorded_data_intensity = list(
                rating_intensity.dato_calificacion.all())

            if not recorded_data_intensity or len(recorded_data_intensity) < len(words):
                use_product = current_product
                break


        # Si no hay productos pendientes, pasar a Fase 2
        if not products_pending and use_product is None:
            params = {"code_sesion": self.session.codigo_sesion}
            return redirect(reverse("cata_system:session_perfil_ideal_phase2", kwargs=params))

        # Seleccionar producto aleatoriamente de los pendientes
        if use_product is None:
            use_product = random.choice(products_pending)

        # Verificar qué palabras faltan por calificar para este producto
        try:
            rating_intensity = ratings_dict[use_product.id].get(
                scales_by_type.get("estructurada").id)

            recorded_data = rating_intensity.dato_calificacion.all()
            use_words = PalabrasController.getWordsWithoutData(
                recoreded_data=recorded_data, words=words)
        except Exception as e:
            use_words = words

        self.context["product"] = use_product
        self.context["words"] = use_words
        self.context["intensity_scale"] = scales_by_type.get("estructurada")
        self.context["ideal_scale"] = scales_by_type.get("ideal")
        self.context["scale_size"] = scales_by_type.get("estructurada").longitud

        return render(request, self.current_directory, self.context)
