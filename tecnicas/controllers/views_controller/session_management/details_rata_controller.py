from django.http import HttpRequest
from django.shortcuts import render, redirect
from tecnicas.models import SesionSensorial
from tecnicas.controllers import PalabrasController, DatoController, CalificacionController
from tecnicas.utils import defaultdict_to_dict
from .details_controller import DetallesController
from collections import defaultdict


class DetallesRATAController(DetallesController):
    def __init__(self, session: SesionSensorial):
        super().__init__(session)

    def getResponse(self, request: HttpRequest, error: str = ""):
        context = self.getContext()
        if error != "" or error:
            context["error"] = error
        return render(
            request, self.url_template, context)

    def getContext(self):
        self.context = {}
        self.context["sesion"] = self.session
        self.words = PalabrasController.getWordsInTechnique(
            self.session.tecnica)
        self.context["palabras"] = [word.nombre_palabra for word in self.words]

        ratings_for_repetition = []

        ratings = CalificacionController.getRatingsByTechnique(
            technique=self.session.tecnica)

        if isinstance(ratings, dict) or not ratings:
            self.context["calificaciones"] = ratings_for_repetition
            self.context["existen_calificaciones"] = False
            return self.context

        data = DatoController.getWordValuesForConvecional(
            ratings=ratings, technique=self.session.tecnica)

        ratings_for_repetition = defaultdict(
            lambda: defaultdict(lambda: defaultdict(list)))

        for item in data:
            user = item["usuarioCatador"]
            rep = item["repeticion"]
            prod = item["producto_code"]

            ratings_for_repetition[rep][user][prod].append({
                "nombre_palabra": item["nombre_palabra"],
                "dato_valor": item["dato_valor"]
            })

        self.context["calificaciones"] = defaultdict_to_dict(
            ratings_for_repetition)
        self.context["existen_calificaciones"] = True
