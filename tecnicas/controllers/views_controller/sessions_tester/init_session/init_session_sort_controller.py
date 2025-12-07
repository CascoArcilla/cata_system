from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from tecnicas.models import Participacion
from tecnicas.controllers import ParticipacionController
from .init_session_controller import InitSessionController


class InitSessionSortController(InitSessionController):
    def __init__(self, sensorial_session, user_tester):
        super().__init__(sensorial_session, user_tester)
        self.current_direction = "tecnicas/forms_tester/init_test_sort.html"
        self.sort_direction = "cata_system:session_sort"

    def controllGet(self, request: HttpRequest, error=""):
        context = {
            "session": self.session,
            "type_technique": self.session.tecnica.tipo_tecnica.nombre_tecnica
        }

        is_end = self.isEndedSession()

        context["has_ended"] = is_end

        if is_end:
            context["message"] = "El catador ha terminado de realizar su evaluación, espere instrucciones del presentador"

        if "error" in request.GET:
            context["error"] = request.GET["error"]

        return render(request, self.current_direction, context)

    def isEndedSession(self):
        participation = Participacion.objects.get(
            catador=self.tester, tecnica=self.session.tecnica)

        return participation.finalizado

    def controllPost(self, request: HttpRequest):
        context = {
            "session": self.session,
            "type_technique": self.session.tecnica.tipo_tecnica.nombre_tecnica
        }

        use_action = request.POST["action"]

        if use_action == "start_posting":
            parameters = {
                "code_sesion": self.session.codigo_sesion
            }

            is_end = self.isEndedSession()
            if is_end:
                context["message"] = "El catador ha terminado de realizar su evaluación, espere instrucciones del presentador"
                return render(request, self.current_direction, context)

            update_participation = ParticipacionController.enterSession(
                tester=request.user.user_catador, session=self.session)

            if isinstance(update_participation, dict):
                context["error"] = update_participation["error"]
                return render(request, self.current_direction, context)

            request.session["id_participation"] = update_participation.id

            return redirect(reverse(self.sort_direction, kwargs=parameters))

        elif use_action == "exit_session":
            response = ParticipacionController.outSession(
                tester=request.user.user_catador, session=self.session)
            if isinstance(response, dict):
                context["error"] = response["error"]
            return render(request, self.current_direction, context)

        else:
            context["error"] = "Acción sin especificar"
            return render(request, self.current_direction, context)
