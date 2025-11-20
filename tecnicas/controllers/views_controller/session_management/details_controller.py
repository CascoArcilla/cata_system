from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from tecnicas.models import SesionSensorial, Presentador, Tecnica, Participacion
from tecnicas.controllers import ParticipacionController


class DetallesController():
    url_template: str
    url_next: str

    def __init__(self, session: SesionSensorial):
        self.session = session

    def controllGetResponse(self, request: HttpRequest, error: str = "", message: str = ""):
        context = self.getContext()

        if error != "" or error:
            context["error"] = error
        if message != "" or message:
            context["message"] = message

        return render(
            request, self.url_template, context)

    def getContext(self):
        return {}

    def deleteSesorialSession(self):
        technique = Tecnica.objects.get(id=self.session.tecnica.id)
        technique.delete()

    def startRepetition(self, presenter: Presentador, request: HttpRequest):
        creator = presenter
        technique = self.session.tecnica

        if creator.user.username != self.session.creadoPor.user.username:
            return self.controllGetResponse(error="Solo el presentador que crea la sesión puede iniciar la repetición", request=request)
        elif self.session.activo:
            return self.controllGetResponse(error="La sesión ya está activada", request=request)
        elif technique.repeticion >= technique.repeticiones_max:
            return self.controllGetResponse(error="Se ha alcanzado el número de repeticiones máxima", request=request)

        there_participacions = Participacion.objects.filter(
            tecnica=technique).exists()

        if there_participacions:
            (is_update_participations,
             message) = ParticipacionController.outAllInSession(self.session)
            if not is_update_participations:
                return self.controllGetResponse(error=message, request=request)

        self.session.activo = True
        technique.repeticion = technique.repeticion + 1

        technique.save()
        self.session.save()

        parameters = {
            "session_code": self.session.codigo_sesion
        }
        return redirect(
            reverse(self.url_next, kwargs=parameters))
