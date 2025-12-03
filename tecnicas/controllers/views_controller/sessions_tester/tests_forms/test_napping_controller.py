from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from django.db.models import F
from tecnicas.models import Participacion, Producto, TecnicaModalidad, DatoPunto, Calificacion, Modalidad
from tecnicas.forms import ListWordsForm
from tecnicas.utils import noValidTechnique
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
            tecnica=technique, usando=True).modalidad.nombre

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
            tecnica=self.session.tecnica,
            modalidad=Modalidad.objects.get(nombre="sin modalidad")
        )

        self.context["maked_napping"] = True if maked_previus_napping else False
        self.context["mode"] = "perfil ultra flash"
        self.context["form"] = ListWordsForm()

        self.context["session"] = self.session
        technique = self.session.tecnica
        products_in_technique = Producto.objects.filter(id_tecnica=technique)
        self.context["products"] = products_in_technique
        self.setCoordinates()

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
            id_product=F("calificacion__id_producto")
        )

        self.context["data_points"] = list(data_points)
