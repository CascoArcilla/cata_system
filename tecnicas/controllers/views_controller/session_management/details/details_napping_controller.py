from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from .details_controller import DetallesController
from tecnicas.models import SesionSensorial, Presentador, Modalidad
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

        modes = Modalidad.objects.all()
        technique_modes = self.session.tecnica.modalidad.all()

        if not technique_modes.exists():
            self.context["modes"] = modes
        else:
            use_modes = technique_modes.values_list("id", flat=True)

            self.context["modes"] = modes.exclude(
                id__in=use_modes)

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
        print(action)
        if action == "start_sin_modalidad":
            response = self.startNapping(request=request)

        elif action == "delete_session":
            self.deleteSesorialSession()
            response = redirect(
                reverse("cata_system:panel_sesiones", kwargs={"page": 1}))

        else:
            response= self.controllGetResponse(
                error="Modalidad sin implantar", request=request)

        return response

    def startNapping(self, request: HttpRequest):
        if request.user.user_presentador.user.username != self.session.creadoPor.user.username:
            return self.controllGetResponse(error="Solo el presentador que crea la sesión puede iniciar la repetición", request=request)
        elif self.session.activo:
            return self.controllGetResponse(error="La sesión ya está activada", request=request)

        self.session.activo = True
        self.session.save()

        parameters = {
            "session_code": self.session.codigo_sesion
        }
        return redirect(
            reverse(self.url_next, kwargs=parameters))
