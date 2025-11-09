from django.http import HttpRequest
from django.shortcuts import render, redirect
from tecnicas.models import SesionSensorial
from tecnicas.controllers import PalabrasController, DatoController, CalificacionController
from tecnicas.utils import defaultdict_to_dict
from .details_controller import DetallesController
from collections import defaultdict


class DetallesCATAController(DetallesController):
    def __init__(self, session: SesionSensorial):
        super().__init__(session)
        self.url_template = "tecnicas/manage_sesions/detalles-sesion-cata.html"
        self.url_next = "cata_system:monitor_sesion"

    def getContext(self):
        technique = self.session.tecnica

        self.context = {
            "sesion": self.session,
            "use_technique": technique
        }

        # Recuperar palabras
        self.words = PalabrasController.getWordsInTechnique(
            self.session.tecnica)
        self.context["palabras"] = [word.nombre_palabra for word in self.words]

        # Intentar recuperar las calificaciones
        ratings_for_repetition = []

        ratings = CalificacionController.getRatingsByTechnique(
            technique=technique)

        if isinstance(ratings, dict) or not ratings:
            self.context["calificaciones"] = ratings_for_repetition
            self.context["existen_calificaciones"] = False
            return self.context

        data = DatoController.getWordValuesForConvecional(
            ratings=ratings, technique=technique)

        ratings_for_repetition = defaultdict(
            lambda: defaultdict(lambda: defaultdict(list)))

        for item in data:
            user = item["usuario_catador"]
            rep = item["repeticion"]
            prod = item["producto_code"]

            ratings_for_repetition[rep][user][prod].append({
                "nombre_palabra": item["nombre_palabra"],
                "dato_valor": item["dato_valor"]
            })

        self.context["calificaciones"] = defaultdict_to_dict(
            ratings_for_repetition)
        self.context["existen_calificaciones"] = True

        # Se comprueba que ya no se pueda iniciar la repeticion
        self.context["fin_repeticiones"] = technique.repeticion >= technique.repeticiones_max
        return self.context
