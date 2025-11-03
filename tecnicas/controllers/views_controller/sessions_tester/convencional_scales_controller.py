from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from tecnicas.models import SesionSensorial, Catador, Participacion, Producto
from tecnicas.controllers import PosicionController, CalificacionController, ParticipacionController, PalabrasController, EscalaController, DatoController


class ConvencionalScalesController:
    context = {}
    current_directory = "tecnicas/forms_tester/convencional.html"

    def __init__(self, sensorial_session: SesionSensorial, user_tester: Catador):
        self.tester = user_tester
        self.session = sensorial_session

    def controllGetEscalas(self, request: HttpRequest):
        technique = self.session.tecnica
        self.participation = Participacion.objects.get(
            tecnica=technique, catador=request.user.user_catador)

        self.context["session"] = self.session

        positions = PosicionController.getPostionsInOrder(
            id_order=request.session["id_order"])

        sorted_positions = sorted(positions, key=lambda posi: posi.posicion)

        words = PalabrasController.getWordsInTechnique(technique=technique)

        next_position = CalificacionController.checkProducsWithoutRating(
            positions=sorted_positions,
            user_cata=request.user.username,
            id_technique=technique.id,
            repetition=technique.repeticion,
            technique=technique,
            num_words=len(words)
        )

        if isinstance(next_position, dict):
            updated_participation = ParticipacionController.finishSession(
                self.participation)
            params = {
                "code_sesion": self.session.codigo_sesion
            }
            return redirect(reverse('cata_system:catador_init_session', kwargs=params))

        if isinstance(next_position, list):
            next_position = next_position[0]

        self.context["product"] = next_position.id_producto

        ratings_product = CalificacionController.getRatings(
            technique=technique,
            product=next_position.id_producto,
            repetition=technique.repeticion,
            user_tester=request.user.username
        )

        if isinstance(ratings_product, dict):
            self.context["error"] = ratings_product["error"]
            return render(request, self.current_directory, self.context)
        elif not ratings_product:
            self.context["words"] = words
        else:
            recoreded_data = DatoController.getRerecordedData(
                ratings=ratings_product)
            if not recoreded_data:
                self.context["words"] = words
            else:
                words_to_use = PalabrasController.getWordsWithoutData(
                    recoreded_data=recoreded_data, words=words)
                self.context["words"] = words_to_use

        scale = EscalaController.getScaleByTechnique(technique=technique)
        self.context["scale"] = scale
        self.context["type_scale"] = scale.id_tipo_escala.nombre_escala

        use_tags = EscalaController.getRelatedTagsInScale(scale=scale)
        self.context["tags"] = use_tags

        print(self.context)
        return render(request, self.current_directory, self.context)

    def controllGetRATA(self, request: HttpRequest):
        technique = self.session.tecnica
        self.participation = Participacion.objects.get(
            tecnica=technique, catador=request.user.user_catador)

        self.context["session"] = self.session

        products_in_technique = Producto.objects.filter(id_tecnica=technique)

        words = PalabrasController.getWordsInTechnique(technique=technique)

        # Revisamos el producto que le falten calificaciones
        for product_in in products_in_technique:
            ratings_product = CalificacionController.getRatings(
                technique=technique,
                product=product_in,
                repetition=technique.repeticion,
                user_tester=request.user.username
            )

            if isinstance(ratings_product, dict):
                self.context["error"] = ratings_product.get("error")
                return render(request, self.current_directory, self.context)

            # Sin calificaciones mandamos el producto actual y todas la palabras
            if not ratings_product:
                self.context["product"] = product_in
                self.context["words"] = words
                break

            # Obtener los datos asociados parala calificacion para ver que palabras quedan por calificar
            recoreded_data = DatoController.getRerecordedData(ratings=ratings_product)

            if not recoreded_data:
                # Si no hay datos entonces devolver el producto con todas las palabras
                self.context["product"] = product_in
                self.context["words"] = words
                break
            else:
                words_to_use = PalabrasController.getWordsWithoutData(
                    recoreded_data=recoreded_data, words=words)

                # Si quedan palabras por calificar mandar las palabras con el producto
                if not isinstance(words_to_use, dict) and words_to_use:
                    self.context["product"] = product_in
                    self.context["words"] = words_to_use
                    break

        # Si no hay producto que falta por calificar finalizar sesion para el Catador
        if "product" not in self.context:
            updated_participation = ParticipacionController.finishSession(
                self.participation)
            params = {
                "code_sesion": self.session.codigo_sesion
            }
            return redirect(reverse('cata_system:catador_init_session', kwargs=params))

        # Agregar informacion de la escala
        scale = EscalaController.getScaleByTechnique(technique=technique)
        self.context["scale"] = scale
        self.context["type_scale"] = scale.id_tipo_escala.nombre_escala

        use_tags = EscalaController.getRelatedTagsInScale(scale=scale)
        self.context["tags"] = use_tags

        return render(request, self.current_directory, self.context)
