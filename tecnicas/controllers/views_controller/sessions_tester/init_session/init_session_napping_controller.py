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
        self.napping_direction = "cata_system:session_napping"

    def controllGet(self, request: HttpRequest):
        self.context = {
            "session": self.session,
            "type_technique": "napping",
            "has_ended": self.isEndedSession()
        }

        if self.session.tecnica.repeticion == 1:
            self.context["status"] = "En esta sesión se usará Napping"
        else:
            self.context["status"] = "Se uso Napping puro en la última sesión"

        if "error" in request.GET:
            self.context["error"] = request.GET["error"]

        return render(request, self.current_direction, self.context)

    def isEndedSession(self):
        return Participacion.objects.get(
            tecnica=self.session.tecnica, catador=self.tester).finalizado

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

            return redirect(reverse(self.napping_direction, kwargs=parameters))

        elif use_action == "exit_session":
            response = ParticipacionController.outSession(
                tester=request.user.user_catador, session=self.session)
            if isinstance(response, dict):
                context["error"] = response["error"]
            return render(request, self.current_direction, context)

        else:
            context["error"] = "Acción sin especificar"
            return render(request, self.current_direction, context)
