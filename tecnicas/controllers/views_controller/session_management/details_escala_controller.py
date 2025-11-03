'''

Para Tecnicas Convencionales, CATA, RATA, Escala Hedonica
Encabezados de como deben de aparecer los datos por repeticion

| Repeticion: R
| Codigo Producto | Catador | P1 | P2 | P3 | Pn |

Encabezados de como deben de aparecer los datos juntos

| Repeticion | Codigo Producto | Catador | P1 | P2 | P3 | Pn |

'''
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from tecnicas.models import SesionSensorial, Presentador, Participacion
from tecnicas.controllers import DatoController, CalificacionController, PalabrasController, ParticipacionController
from .details_controller import DetallesController
from tecnicas.utils import defaultdict_to_dict, controller_error
from collections import defaultdict


class DetallesEscalasController(DetallesController):
    url_template = "tecnicas/manage_sesions/detalles-sesion.html"

    def __init__(self, session: SesionSensorial):
        super().__init__(session)

    def getResponse(self, request: HttpRequest, error: str = "", message: str = ""):
        context = self.getContext()

        if error != "" or error:
            context["error"] = error
        if message != "" or message:
            context["message"] = message

        return render(
            request, self.url_template, context)

    def getContext(self):
        self.context = {
            "use_technique": self.session.tecnica.tipo_tecnica.nombre_tecnica
        }
        self.context["sesion"] = self.session

        # Recuperar la palabras de la tecnica
        self.words = PalabrasController.getWordsInTechnique(
            self.session.tecnica)
        self.context["palabras"] = [word.nombre_palabra for word in self.words]

        # Se recuperan las calificaciones
        ratings_for_repetition = []

        ratings = CalificacionController.getRatingsByTechnique(
            technique=self.session.tecnica)

        if isinstance(ratings, dict) or not ratings:
            self.context["calificaciones"] = ratings_for_repetition
            self.context["existen_calificaciones"] = False
            return self.context

        data = DatoController.getWordValuesForConvecional(
            ratings=ratings, technique=self.session.tecnica)

        ratings_for_repetition = defaultdict(
            lambda: defaultdict(lambda: defaultdict(list)))

        for item in data:
            user = item["usuarioCatador"]
            rep = item["repeticion"]
            prod = item["producto_code"]

            ratings_for_repetition[rep][user][prod].append({
                "nombre_palabra": item["nombre_palabra"],
                "dato_valor": item["dato_valor"]
            })

        self.context["calificaciones"] = defaultdict_to_dict(
            ratings_for_repetition)
        self.context["existen_calificaciones"] = True

        # Se comprueba que ya no se pueda iniciar la repeticion
        self.context["fin_repeticiones"] = self.session.tecnica.repeticion >= self.session.tecnica.repeticiones_max

        return self.context

    def startRepetition(self, presenter: Presentador, request: HttpRequest):
        creator = presenter
        technique = self.session.tecnica

        if creator.user.username != self.session.creadoPor.user.username:
            return self.getResponse(error="Solo el presentador que crea la sesión puede iniciar la repetición", request=request)
        elif self.session.activo:
            return self.getResponse(error="La sesión ya está activada", request=request)
        elif technique.repeticion >= technique.repeticiones_max:
            return self.getResponse(error="Se ha alcanzado el número de repeticiones máxima", request=request)
        
        there_participacions = Participacion.objects.filter(tecnica=technique).exists()

        if there_participacions:
            (is_update_participations,
            message) = ParticipacionController.outAllInSession(self.session)
            if not is_update_participations:
                return self.getResponse(error=message, request=request)

        self.session.activo = True
        technique.repeticion = technique.repeticion + 1

        technique.save()
        self.session.save()

        parameters = {
            "session_code": self.session.codigo_sesion
        }
        return redirect(
            reverse("cata_system:monitor_sesion", kwargs=parameters))
