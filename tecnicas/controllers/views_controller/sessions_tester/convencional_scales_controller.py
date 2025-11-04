from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from tecnicas.models import SesionSensorial, Catador, Participacion, Producto, Calificacion, Palabra
from tecnicas.controllers import PosicionController, CalificacionController, ParticipacionController, PalabrasController, EscalaController, DatoController


class ConvencionalScalesController:
    context = {}
    current_directory = "tecnicas/forms_tester/convencional.html"
    previus_directory = "cata_system:catador_init_session"

    def __init__(self, sensorial_session: SesionSensorial, user_tester: Catador):
        self.tester = user_tester
        self.session = sensorial_session

    def controllGetEscalas(self, request: HttpRequest):
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

        return render(request, self.current_directory, ctx)

    def controllGetRATA(self, request: HttpRequest):
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
                there_rating = True
            except Calificacion.DoesNotExist:
                there_rating = False

            # Si no hay calificacion mandamos el producto actual y todas la palabras
            if not there_rating:
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

        return render(request, self.current_directory, self.context)
