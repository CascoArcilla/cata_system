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
        self.setOptionesMode()
        self.setDataTableNoMode()

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
        if action == "start_sin_modalidad":
            name_mode = action.replace("start_", "").replace("_", " ")
            response = self.startNapping(request=request, name_mode=name_mode)

        if action == "start_perfil_ultra_flash":
            name_mode = action.replace("start_", "").replace("_", " ")
            return self.controllGetResponse(error="Trabajando en la modalidad", request=request)

        elif action == "delete_session":
            self.deleteSesorialSession()
            response = redirect(
                reverse("cata_system:panel_sesiones", kwargs={"page": 1}))

        else:
            response = self.controllGetResponse(
                error="Modalidad sin implantar", request=request)

        return response

    def startNapping(self, request: HttpRequest, name_mode: str):
        if request.user.user_presentador.user.username != self.session.creadoPor.user.username:
            return self.controllGetResponse(error="Solo el presentador que crea la sesión puede iniciar la repetición", request=request)
        elif self.session.activo:
            return self.controllGetResponse(error="La sesión ya está activada", request=request)

        tecnique_mode = TecnicaModalidad.objects.get_or_create(
            tecnica=self.session.tecnica, modalidad=Modalidad.objects.get(nombre=name_mode), usando=True)

        if not tecnique_mode:
            return self.controllGetResponse(error="Modalidad no encontrada", request=request)

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

    def setOptionesMode(self):
        modes = Modalidad.objects.all()
        technique_modes = TecnicaModalidad.objects.filter(
            tecnica=self.session.tecnica)

        if not technique_modes.exists():
            self.context["modes"] = modes
        else:
            use_modes = technique_modes.values_list("modalidad", flat=True)

            self.context["modes"] = modes.exclude(
                id__in=use_modes)
