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
        self.setDataTable()

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

    def setDataTable(self):
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

        # Add word frequency data for perfil ultra flash mode
        mod = TecnicaModalidad.objects.get(tecnica=self.session.tecnica)
        if mod.modalidad.nombre == "perfil ultra flash":
            self.setWordFrequencies(ratings)

        self.context["there_data"] = True

    def setWordFrequencies(self, ratings):
        from collections import Counter
        
        # Prefetch palabras to optimize queries
        ratings_with_words = ratings.prefetch_related('palabras').select_related('id_producto')
        
        # Dictionary to store word frequencies by product
        word_frequencies_by_product = defaultdict(Counter)
        all_words_set = set()
        
        for rating in ratings_with_words:
            producto_code = rating.id_producto.codigoProducto
            words = rating.palabras.all()
            
            for word in words:
                word_name = word.nombre_palabra
                word_frequencies_by_product[producto_code][word_name] += 1
                all_words_set.add(word_name)
        
        # Convert Counter objects to regular dicts and sort words alphabetically
        word_frequencies_dict = {
            product: dict(frequencies)
            for product, frequencies in word_frequencies_by_product.items()
        }
        
        # Sort all words alphabetically for consistent column ordering
        all_words_sorted = sorted(all_words_set)
        
        self.context["word_frequencies"] = word_frequencies_dict
        self.context["all_words"] = all_words_sorted

    def setIsEndSession(self):
        if not self.session.activo and self.session.tecnica.repeticion < 1:
            self.context["finished"] = False
            return
        elif self.session.activo:
            self.context["finished"] = False
            return
        elif not self.session.activo and self.session.tecnica.repeticion >= 1:
            self.context["finished"] = True
            return
