from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from django.db.models import F
from tecnicas.models import Participacion, Producto, TecnicaModalidad, DatoPunto, Calificacion, Modalidad, Palabra
from tecnicas.forms import ListWordsForm
from tecnicas.utils import noValidTechnique
from tecnicas.controllers import ParticipacionController
from .general_test_controller import GenetalTestController


class TestNappingController(GenetalTestController):
    def __init__(self, sensorial_session, user_tester):
        super().__init__(sensorial_session, user_tester)
        self.napping_test = "tecnicas/forms_tester/test_napping.html"
        self.napping_puf_test = "tecnicas/forms_tester/test_napping_puf.html"

    def controllGet(self, request: HttpRequest):
        technique = self.session.tecnica

        self.participation = Participacion.objects.get(
            tecnica=technique, catador=request.user.user_catador)

        # Comprobar que el Catador no haya finalizado
        if self.participation.finalizado:
            params = {
                "code_sesion": self.session.codigo_sesion
            }
            return redirect(reverse(self.previus_directory, kwargs=params))

        name_mode_activate = TecnicaModalidad.objects.get(
            tecnica=technique).modalidad.nombre

        if name_mode_activate == "sin modalidad":
            self.context["mode"] = "sin modalidad"
            return self.nappingTest(request)
        if name_mode_activate == "perfil ultra flash":
            self.context["mode"] = "perfil ultra flash"
            return self.nappingPufTest(request)
        else:
            return noValidTechnique(
                name_view=self.previus_directory,
                query_params={
                    "error": f"Trabajando en la modalidad: {name_mode_activate}"
                },
                params={
                    "code_sesion": self.session.codigo_sesion
                }
            )

    def nappingTest(self, request: HttpRequest):
        self.context["session"] = self.session
        technique = self.session.tecnica

        products_in_technique = Producto.objects.filter(id_tecnica=technique)
        self.context["products"] = products_in_technique

        self.setCoordinates()

        return render(request, self.napping_test, self.context)

    def nappingPufTest(self, request: HttpRequest):
        maked_previus_napping = TecnicaModalidad.objects.get(
            tecnica=self.session.tecnica)

        self.context["maked_napping"] = True if maked_previus_napping else False
        self.context["mode"] = "perfil ultra flash"
        self.context["form"] = ListWordsForm()

        self.context["session"] = self.session
        technique = self.session.tecnica
        products_in_technique = Producto.objects.filter(id_tecnica=technique)
        self.context["products"] = products_in_technique
        self.setCoordinates()
        self.setWords()

        return render(request, self.napping_puf_test, self.context)

    def setCoordinates(self):
        technique = self.session.tecnica

        ratings = Calificacion.objects.filter(
            num_repeticion=0,
            id_tecnica=technique,
            id_catador=self.participation.catador
        )

        data_points = DatoPunto.objects.filter(
            calificacion__in=ratings
        ).values(
            code=F("calificacion__id_producto__codigoProducto"),
            px=F("x"),
            py=F("y"),
            id_product=F("calificacion__id_producto__id")
        )

        self.context["data_points"] = list(data_points)

    def setWords(self):
        technique = self.session.tecnica

        ratings = Calificacion.objects.filter(
            num_repeticion=0,
            id_tecnica=technique,
            id_catador=self.participation.catador
        ).prefetch_related('palabras', 'id_producto')

        words_by_product = {}
        for rating in ratings:
            product_code = rating.id_producto.codigoProducto
            words_list = list(rating.palabras.values_list(
                'nombre_palabra', flat=True))
            if words_list:
                words_by_product[product_code] = words_list

        self.context["words_by_product"] = words_by_product

    def controllPost(self, request: HttpRequest):
        action = request.POST.get("action")

        if action == "finish_session":
            # Get technique and mode
            technique = self.session.tecnica
            self.participation = Participacion.objects.get(
                tecnica=technique, catador=request.user.user_catador)

            name_mode_activate = TecnicaModalidad.objects.get(
                tecnica=technique).modalidad.nombre

            # Validate based on mode
            validation_error = self.validateSessionCompletion(
                technique, name_mode_activate)

            if validation_error:
                # Return to the appropriate template with error
                if name_mode_activate == "sin modalidad":
                    return self.nappingTest(request)
                elif name_mode_activate == "perfil ultra flash":
                    return self.nappingPufTest(request)

            # If validation passes, finish the session
            ParticipacionController.finishSession(self.participation)
            params = {"code_sesion": self.session.codigo_sesion}
            return redirect(reverse(self.previus_directory, kwargs=params))

        # For other actions, call parent's controllPost
        return super().controllPost(request)

    def validateSessionCompletion(self, technique, mode_name):
        # Get all products in technique
        products = Producto.objects.filter(id_tecnica=technique)
        product_count = products.count()

        # Get all ratings for this tester
        ratings = Calificacion.objects.filter(
            num_repeticion=0,
            id_tecnica=technique,
            id_catador=self.participation.catador
        ).select_related('id_producto').prefetch_related('palabras')

        # Check if all products have ratings
        if ratings.count() != product_count:
            missing_count = product_count - ratings.count()
            return f"Faltan {missing_count} producto(s) por evaluar."

        # Check if all ratings have DatoPunto (coordinates)
        ratings_with_points = DatoPunto.objects.filter(
            calificacion__in=ratings
        ).values_list('calificacion_id', flat=True)

        ratings_without_points = ratings.exclude(id__in=ratings_with_points)
        if ratings_without_points.exists():
            missing_products = [
                r.id_producto.codigoProducto for r in ratings_without_points
            ]
            return f"Los siguientes productos no tienen coordenadas: {', '.join(missing_products)}"

        # Additional validation for "perfil ultra flash" mode
        if mode_name == "perfil ultra flash":
            # Check that each rating has at least one word
            ratings_without_words = []
            for rating in ratings:
                if rating.palabras.count() < 1:
                    ratings_without_words.append(
                        rating.id_producto.codigoProducto)

            if ratings_without_words:
                return f"Los siguientes productos deben tener al menos 1 palabra: {', '.join(ratings_without_words)}"

        # All validations passed
        return None
