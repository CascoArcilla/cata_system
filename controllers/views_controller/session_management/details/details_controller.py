from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from tecnicas.models import SesionSensorial, Presentador, Tecnica, Participacion
from controllers import ParticipacionController


class DetallesController():
    url_template: str
    url_next = "cata_system:monitor_sesion"

    def __init__(
        self,
        session: SesionSensorial,
        back_url: str = "cata_system:panel_sesiones",
        home_url: str = "cata_system:index"
    ):
        self.session = session
        self.back_url = back_url
        self.home_url = home_url

    def controllGetResponse(self, request: HttpRequest, error: str = "", message: str = ""):
        context = self.getContext()

        if error != "" or error:
            context["error"] = error
        if message != "" or message:
            context["message"] = message

        if request.session.get("technique_selected") == "general":
            self.back_url = "cata_system:panel_sesiones"
            self.home_url = "cata_system:index"

        context["back_url"] = reverse(self.back_url, kwargs={"page": 1})
        context["home_url"] = reverse(self.home_url)

        if context["technique"].get("words_style") == "vocabulario":
            context["name_vocabulary"] = self.session.tecnica.tecnica_esvacabulario.id_vocabulario.nombre_vocabulario

        return render(
            request, self.url_template, context)

    def controllPostResponse(self, request: HttpRequest, action: str):
        if action == "start_session":
            return self.startRepetition(
                presenter=request.user.user_presentador, request=request)

        elif action == "delete_session":
            self.deleteSesorialSession()
            return redirect(
                reverse(self.back_url, kwargs={"page": 1}))

        else:
            return self.controllGetResponse(error="Acción no reconocida", request=request)

    def getContext(self):
        return {}

    def deleteSesorialSession(self):
        technique = Tecnica.objects.get(id=self.session.tecnica.id)
        technique.delete()

    def startRepetition(self, presenter: Presentador, request: HttpRequest):
        creator = presenter
        technique = self.session.tecnica

        if creator.user.username != self.session.creadoPor.user.username:
            return self.controllGetResponse(error="Solo el analista que crea la sesión puede iniciar la repetición", request=request)
        elif self.session.activo:
            return self.controllGetResponse(error="La sesión ya está activada", request=request)
        elif technique.repeticion >= technique.repeticiones_max:
            return self.controllGetResponse(error="Se ha alcanzado el número de repeticiones máxima", request=request)

        is_update_participations = self.setParticipationsToNoFinished()
        if not is_update_participations:
            return self.controllGetResponse(error="Error al actualizar las participaciones", request=request)

        self.session.activo = True
        technique.repeticion = technique.repeticion + 1

        technique.save()
        self.session.save()

        parameters = {
            "session_code": self.session.codigo_sesion
        }
        return redirect(
            reverse(self.url_next, kwargs=parameters))

    def setParticipationsToNoFinished(self):
        there_participacions = Participacion.objects.filter(
            tecnica=self.session.tecnica).exists()

        if there_participacions:
            (is_update_participations,
             message) = ParticipacionController.outAllInSession(self.session)

            return is_update_participations

        return True
