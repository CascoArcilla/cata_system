from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from tecnicas.models import SesionSensorial, Producto, EsAtributo, EsVocabulario, Participacion
from tecnicas.controllers import ParticipacionController


class MonitorController():
    url_view: str
    previus_view: str

    def __init__(self, session: SesionSensorial, url_home="cata_system:index"):
        self.sensorial_session = session
        self.url_home = url_home

    def controllPostFinishSession(self, request: HttpRequest):
        (is_all_end, message) = self.checkAllFinish()
        if not is_all_end:
            self.setContext()
            if request.session.get("technique_selected") == "general":
                self.context["url_home"] = reverse("cata_system:index")

            self.context["error"] = message
            return render(request, self.url_view, self.context)

        self.finishSession()
        return redirect(reverse(self.previus_view, kwargs={"session_code": self.sensorial_session.codigo_sesion}))

    def checkAllFinish(self) -> (bool, str):
        return (False, "Función sin implementar")

    def setContext(self):
        ParticipacionController.checkStaleParticipations(
            self.sensorial_session.tecnica, 600)

        self.participations = Participacion.objects.filter(
            tecnica=self.sensorial_session.tecnica)

        self.context = {
            "code_session": self.sensorial_session.codigo_sesion,
            "session_name": self.sensorial_session.nombre_sesion,
            "max_testers": self.sensorial_session.tecnica.limite_catadores,
            "current_testers": len(self.participations),
            "active_testers": len([part for part in self.participations if part.activo]),
            "participations": self.participations,
            "use_technique": self.sensorial_session.tecnica.tipo_tecnica.nombre_tecnica,
            "url_home": reverse(self.url_home)
        }

    def controllGetResponse(self, request: HttpRequest,  error: str = "", message: str = ""):
        self.setContext()

        if error != "" or error:
            self.context["error"] = error
        if message != "" or message:
            self.context["message"] = message

        if request.session.get("technique_selected") == "general":
            self.context["url_home"] = reverse("cata_system:index")

        return render(request, self.url_view, self.context)

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

    def finishSession(self):
        self.sensorial_session.activo = False
        self.sensorial_session.save()
        return self.sensorial_session
