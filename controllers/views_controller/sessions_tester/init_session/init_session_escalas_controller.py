from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from tecnicas.models import Catador, SesionSensorial, Orden
from controllers import ParticipacionController
from .init_session_controller import InitSessionController


class InitSessionEscalasController(InitSessionController):
    tester: Catador
    session: SesionSensorial
    order: Orden | dict

    def __init__(self, sensorial_session, user_tester):
        super().__init__(sensorial_session, user_tester)
        self.current_direction = "forms_tester/init_scales_test.html"
        self.escalas_direction = "cata_system:session_convencional"
        self.cata_direction = "cata_system:session_cata"

    def controllGet(self, request: HttpRequest):
        context = {
            "session_info": {
                "code": self.session.codigo_sesion,
                "name": self.session.nombre_sesion,
                "instructions": self.session.tecnica.instrucciones,
                "style": self.session.tecnica.id_estilo.nombre_estilo,
                "type_scale": self.session.tecnica.escala_tecnica.all()[0].id_tipo_escala.nombre_escala,
                "repeticion": self.session.tecnica.repeticion
            },
            "use_technique": self.session.tecnica.tipo_tecnica.nombre_tecnica
        }

        order = self.checkAndAssignOrder()
        if isinstance(order, dict):
            context["error"] = order["error"]
            return render(request, self.current_direction, context)

        is_end = self.isEndedSession()

        request.session["id_order"] = order.id
        context["has_ended"] = is_end

        if is_end:
            context["message"] = "El catador ha terminado de realizar su evaluación, espere instrucciones del presentador"

        if "error" in request.GET:
            context["error"] = request.GET["error"]

        return render(request, self.current_direction, context)

    def controllPost(self, request: HttpRequest):
        context = {
            "session_info": {
                "code": self.session.codigo_sesion,
                "name": self.session.nombre_sesion,
                "instructions": self.session.tecnica.instrucciones,
                "style": self.session.tecnica.id_estilo.nombre_estilo,
                "repeticion": self.session.tecnica.repeticion
            },
            "use_technique": self.session.tecnica.tipo_tecnica.nombre_tecnica
        }

        try:
            context["session_info"]["type_scale"] = self.session.tecnica.escala_tecnica.id_tipo_escala.nombre_escala
        except Exception as e:
            context["session_info"]["type_scale"] = None

        if request.POST["action"] == "start_posting":
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

            if self.session.tecnica.tipo_tecnica.nombre_tecnica == "cata":
                return redirect(reverse(self.cata_direction, kwargs=parameters))

            return redirect(reverse(self.escalas_direction, kwargs=parameters))

        elif request.POST["action"] == "exit_session":
            response = ParticipacionController.outSession(
                tester=request.user.user_catador, session=self.session)
            if isinstance(response, dict):
                context["error"] = response["error"]
            return render(request, self.current_direction, context)

        else:
            context["error"] = "Acción sin especificar"
            return render(request, self.current_direction, context)
