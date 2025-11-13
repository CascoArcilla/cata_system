from django.http import HttpRequest
from django.shortcuts import render
from .init_session_controller import InitSessionController


class InitSessionRATAController(InitSessionController):
    def __init__(self, sensorial_session, user_tester):
        super().__init__(sensorial_session, user_tester)
        self.current_direction = "tecnicas/forms_tester/init_session.html"

    def controllGet(self, request: HttpRequest):
        context = {
            "session": self.session,
            "type_technique": self.session.tecnica.tipo_tecnica.nombre_tecnica
        }

        is_end = self.isEndedSession()

        context["has_ended"] = is_end

        if is_end:
            context["message"] = "El catador ha terminado de realizar su evaluación, espere instrucciones del presentador"

        return render(request, self.current_direction, context)
