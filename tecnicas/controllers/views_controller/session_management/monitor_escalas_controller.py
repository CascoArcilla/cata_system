from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from tecnicas.models import SesionSensorial, EsAtributo, EsVocabulario, Producto, Calificacion
from tecnicas.controllers import ParticipacionController, SesionController
from tecnicas.utils import controller_error
from .monitor_controller import MonitorController


class MonitorEscalasController(MonitorController):
    url_view = "tecnicas/manage_sesions/monitor-sesion.html"

    def __init__(self, session: SesionController):
        super().__init__(session)

    def controlGetResponse(self, request: HttpRequest,  error: str = "", message: str = ""):
        self.setContext()

        if error != "" or error:
            self.context["error"] = error
        if message != "" or message:
            self.context["message"] = message

        return render(request, self.url_view, self.context)

    def controlPostResponseFinishSession(self, request: HttpRequest):
        self.setContext()
        (is_all_end, message) = self.checkAllParticipantsEnded()
        if not is_all_end:
            self.context["error"] = message
            return render(request, "tecnicas/manage_sesions/monitor-sesion.html", self.context)
        response = self.finishSession()
        if isinstance(response, dict):
            self.context["error"] = response["error"]
            return render(request, "tecnicas/manage_sesions/monitor-sesion.html", self.context)
        self.context["message"] = message
        return redirect(reverse("cata_system:detalles_sesion", kwargs={"session_code": self.sensorial_session.codigo_sesion}))

    def setContext(self):
        self.participations = ParticipacionController.getParticipationsInTechinique(
            self.sensorial_session.tecnica)

        self.context = {
            "code_session": self.sensorial_session.codigo_sesion,
            "session_name": self.sensorial_session.nombre_sesion,
            "max_testers": self.sensorial_session.tecnica.limite_catadores,
            "current_testers": len(self.participations),
            "active_testers": len([part for part in self.participations if part.activo]),
            "participations": self.participations,
            "use_technique": self.sensorial_session.tecnica.tipo_tecnica.nombre_tecnica
        }

    def getExpectedRatings(self):
        num_products = Producto.objects.filter(
            id_tecnica=self.sensorial_session.tecnica).count()
        style_words = self.sensorial_session.tecnica.id_estilo
        num_words: int

        if style_words.nombre_estilo == "atributos":
            num_words = EsAtributo.objects.get(
                id_tecnica=self.sensorial_session.tecnica).palabras.count()
        elif style_words.nombre_estilo == "vocabulario":
            num_words = EsVocabulario.objects.get(
                id_tecnica=self.sensorial_session.tecnica).id_vocabulario.palabras.count()

        return num_products * num_words

    def checkAllParticipantsEnded(self):
        technique = self.sensorial_session.tecnica

        expected_ratings_repetition = self.getExpectedRatings()

        all_participations = ParticipacionController.getParticipationsInTechinique(
            technique=technique)

        if len(all_participations) < technique.limite_catadores:
            return (False, "No se ha alcanzado el número máximo de Catadores")

        for particiapation in all_participations:
            num_ratings_now = Calificacion.objects.filter(
                id_tecnica=technique, id_catador=particiapation.catador, num_repeticion=technique.repeticion).count()

            if num_ratings_now < expected_ratings_repetition:
                return (False, "No todos los catadores han finalizado su evaluación")

        return (True, "Puedes finalizar la sesión")

    def finishSession(self):
        response = SesionController.finishRepetion(self.sensorial_session)
        if isinstance(response, dict):
            return controller_error(response["error"])
        self.sensorial_session.refresh_from_db()
        return self.sensorial_session
