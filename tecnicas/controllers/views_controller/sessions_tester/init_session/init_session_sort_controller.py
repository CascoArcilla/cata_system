from django.http import HttpRequest
from django.shortcuts import render
from tecnicas.models import Participacion
from .init_session_controller import InitSessionController


class InitSessionSortController(InitSessionController):
    def __init__(self, sensorial_session, user_tester):
        super().__init__(sensorial_session, user_tester)
        self.current_direction = "tecnicas/forms_tester/init_test_sort.html"
        self.pf_direction = "cata_system:session_pf"

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

    def isEndedSession(self):
        participation = Participacion.objects.get(
            catador=self.tester, tecnica=self.session.tecnica)

        return participation.finalizado
