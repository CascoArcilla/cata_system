from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from tecnicas.models import SesionSensorial, Catador


class GenetalTestController():
    previus_directory = "cata_system:catador_init_session"
    context = {}
    current_directory: str

    def __init__(self, sensorial_session: SesionSensorial, user_tester: Catador):
        self.tester = user_tester
        self.session = sensorial_session
