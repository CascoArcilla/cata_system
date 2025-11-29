from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from tecnicas.models import Participacion, Producto, TecnicaModalidad
from tecnicas.utils import noValidTechnique
from .general_test_controller import GenetalTestController


class TestNappingController(GenetalTestController):
    def __init__(self, sensorial_session, user_tester):
        super().__init__(sensorial_session, user_tester)
        self.napping_test = "tecnicas/forms_tester/test_napping.html"

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
            tecnica=technique, usando=True).modalidad.nombre

        if name_mode_activate == "sin modalidad":
            self.context["mode"] = "sin modalidad"
            return self.nappingTest(request)
        else:
            return noValidTechnique(
                name_view=self.previus_directory,
                query_params={
                    "error": "La técnica no tiene modalidad activada"
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

        return render(request, self.napping_test, self.context)
