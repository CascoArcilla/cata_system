from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.db.models import F
from .details_controller import DetallesController
from tecnicas.models import SesionSensorial, Presentador, Modalidad, TecnicaModalidad, Catador, Participacion, DatoPunto, Calificacion
from tecnicas.utils import defaultdict_to_dict
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
        self.setIsEndSession()
        self.setDataTableNoMode()

        return self.context

    def defineStatus(self):
        repetition = self.session.tecnica.repeticion
        mod = TecnicaModalidad.objects.get(
            tecnica=self.session.tecnica)

        self.context["mod_tech"] = mod.modalidad.nombre
        self.context["mode"] = mod.modalidad.nombre
        if mod.modalidad.nombre == "sin modalidad":
            self.context["mod_tech"] = "No se usa modalidad"

        if not self.session.activo:
            self.context["status"] = "Listo para iniciar la sesión con Napping"
        elif self.session.activo:
            self.context["status"] = "Sesión con en curso"

    def controllPostResponse(self, request: HttpRequest, action: str):
        if action == "start_sin_modalidad":
            response = self.startNapping(request=request)

        elif action == "start_perfil_ultra_flash":
            response = self.startNapping(request=request)

        elif action == "delete_session":
            self.deleteSesorialSession()
            response = redirect(
                reverse("cata_system:panel_sesiones", kwargs={"page": 1}))

        else:
            response = self.controllGetResponse(
                error="Modalidad sin implantar", request=request)

        return response

    def startNapping(self, request: HttpRequest):
        if request.user.user_presentador.user.username != self.session.creadoPor.user.username:
            return self.controllGetResponse(error="Solo el presentador que crea la sesión puede iniciar la repetición", request=request)
        elif self.session.activo:
            return self.controllGetResponse(error="La sesión ya está activada", request=request)

        is_update_participations = self.setParticipationsToNoFinished()
        if not is_update_participations:
            return self.controllGetResponse(error="Error al actualizar las participaciones", request=request)

        self.session.activo = True
        self.session.save()

        parameters = {
            "session_code": self.session.codigo_sesion
        }
        return redirect(
            reverse(self.url_next, kwargs=parameters))

    def setDataTableNoMode(self):
        participations = Participacion.objects.filter(
            tecnica=self.session.tecnica).select_related("catador")
        testers = [participation.catador for participation in participations]
        self.context["testers"] = testers

        ratings = Calificacion.objects.filter(id_tecnica=self.session.tecnica)

        coordinates = (
            DatoPunto.objects.filter(calificacion__in=ratings)
            .values(
                producto=F("calificacion__id_producto__codigoProducto"),
                catador=F("calificacion__id_catador__user__username"),
                px=F("x"),
                py=F("y"),
            ))

        if not coordinates.exists():
            self.context["there_data"] = False
            return []

        coordinates_by_product = defaultdict(dict)

        for coordinate in coordinates:
            coordinates_by_product[coordinate["producto"]][coordinate["catador"]] = {
                "px": coordinate["px"],
                "py": coordinate["py"],
            }

        self.context["coordinates_no_mode"] = defaultdict_to_dict(
            coordinates_by_product)

        self.context["there_data"] = True

    def setIsEndSession(self):
        if not self.session.activo:
            self.context["finished"] = False
            return

        participations_finished = Participacion.objects.filter(
            tecnica=self.session.tecnica, finalizado=False).count()

        if participations_finished >= 1:
            self.context["finished"] = False
        else:
            self.context["finished"] = True
