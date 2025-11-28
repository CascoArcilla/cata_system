from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from tecnicas.models import Participacion
from tecnicas.controllers import ParticipacionController
from .init_session_controller import InitSessionController


class InitSessionNappingController(InitSessionController):
    def __init__(self, sensorial_session, user_tester):
        super().__init__(sensorial_session, user_tester)
        self.current_direction = "tecnicas/forms_tester/init_test_napping.html"
        self.sort_direction = "cata_system:session_napping"

    def controllGet(self, request: HttpRequest):
        self.context = {
            "session": self.session,
            "type_technique": "napping",
        }

        if self.session.tecnica.repeticion == 1:
            self.context["status"] = "En esta sesión se usará Napping"
        else:
            self.context["status"] = "Se uso Napping puro en la última sesión"

        if "error" in request.GET:
            self.context["error"] = request.GET["error"]

        return render(request, self.current_direction, self.context)

    def isEndedSession(self):
        pass
