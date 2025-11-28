from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from .details_controller import DetallesController
from tecnicas.models import SesionSensorial, Presentador
from collections import defaultdict


class DetallesNappingController(DetallesController):
    def __init__(self, session: SesionSensorial):
        super().__init__(session)
        self.url_template = "tecnicas/manage_sesions/details-session-napping.html"
        self.url_next = "cata_system:monitor_sesion"

    def getContext(self):
        self.context = {
            "session": self.session,
        }

        self.defineStatus()

        return self.context

    def defineStatus(self):
        repetition = self.session.tecnica.repeticion

        if not repetition and not self.session.activo:
            self.context["status"] = "Listo para iniciar la sesión con Napping"
        elif not repetition and self.session.activo:
            self.context["status"] = "Sesión con Napping en curso"
        elif repetition == 1 and not self.session.activo:
            self.context["status"] = "En espera de la siguiente acción"
        else:
            self.context["status"] = "En espera de la siguiente acción"

    def controllPostResponse(self, request: HttpRequest, action: str):
        if action == "start_session":
            response = self.startRepetition(
                presenter=request.user.user_presentador, request=request)

        elif action == "delete_session":
            self.deleteSesorialSession()
            response = redirect(
                reverse("cata_system:panel_sesiones", kwargs={"page": 1}))

        return response

    def startRepetition(self, presenter: Presentador, request: HttpRequest):
        creator = presenter
        technique = self.session.tecnica

        repetition = technique.repeticion

        if not repetition:
            return self.startNapping(request=request)
        else:
            return self.controllGetResponse(error="Implementación de modalidades en espera", request=request)

    def startNapping(self, request: HttpRequest):
        if request.user.user_presentador.user.username != self.session.creadoPor.user.username:
            return self.controllGetResponse(error="Solo el presentador que crea la sesión puede iniciar la repetición", request=request)
        elif self.session.activo:
            return self.controllGetResponse(error="La sesión ya está activada", request=request)

        self.session.activo = True
        self.session.tecnica.repeticion = self.session.tecnica.repeticion + 1

        self.session.save()
        self.session.tecnica.save()

        parameters = {
            "session_code": self.session.codigo_sesion
        }
        return redirect(
            reverse(self.url_next, kwargs=parameters))
