from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from tecnicas.models import Participacion, TecnicaModalidad
from controllers import ParticipacionController
from .init_session_controller import InitSessionController


class InitSessionNappingController(InitSessionController):
    def __init__(self, sensorial_session, user_tester):
        super().__init__(sensorial_session, user_tester)
        self.current_direction = "forms_tester/init_scales_test.html"
        self.napping_direction = "cata_system:session_napping"
        self.context = {}

    def controllGet(self, request: HttpRequest):        
        self.context = {
            "session_info": {
                "code": self.session.codigo_sesion,
                "name": self.session.nombre_sesion,
                "instructions": self.session.tecnica.instrucciones,
            },
            "use_technique": "napping",
            "has_ended": self.isEndedSession()
        }

        self.setStatusSession()

        if "error" in request.GET:
            self.context["error"] = request.GET["error"]

        return render(request, self.current_direction, self.context)

    def isEndedSession(self):
        return Participacion.objects.get(
            tecnica=self.session.tecnica, catador=self.tester).finalizado

    def controllPost(self, request: HttpRequest):
        self.context = {
            "session_info": {
                "code": self.session.codigo_sesion,
                "name": self.session.nombre_sesion,
                "instructions": self.session.tecnica.instrucciones,
            },
            "use_technique": "napping"
        }

        self.setStatusSession()
        use_action = request.POST["action"]

        if use_action == "start_posting":
            parameters = {
                "code_sesion": self.session.codigo_sesion
            }

            is_end = self.isEndedSession()
            if is_end:
                self.context["message"] = "El catador ha terminado de realizar su evaluación, espere instrucciones del presentador"
                return render(request, self.current_direction, self.context)

            update_participation = ParticipacionController.enterSession(
                tester=request.user.user_catador, session=self.session)

            if isinstance(update_participation, dict):
                self.context["error"] = update_participation["error"]
                return render(request, self.current_direction, self.context)

            request.session["id_participation"] = update_participation.id

            return redirect(reverse(self.napping_direction, kwargs=parameters))

        elif use_action == "exit_session":
            response = ParticipacionController.outSession(
                tester=request.user.user_catador, session=self.session)
            if isinstance(response, dict):
                self.context["error"] = response["error"]
            return render(request, self.current_direction, self.context)

        else:
            self.context["error"] = "Acción sin especificar"
            return render(request, self.current_direction, self.context)

    def setStatusSession(self):
        technique_mode = TecnicaModalidad.objects.get(
            tecnica=self.session.tecnica).modalidad.nombre

        if technique_mode == "posicionamiento":
            self.context["session_info"]["status"] = "La sesión usa Napping"
        else:
            self.context["session_info"]["status"] = f"La sesión usa Napping con modalidad {technique_mode}"
