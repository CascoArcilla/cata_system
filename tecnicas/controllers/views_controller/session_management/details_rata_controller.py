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
