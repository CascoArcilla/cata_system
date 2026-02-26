'''

Para Tecnicas Convencionales, CATA, RATA, Escala Hedonica
Encabezados de como deben de aparecer los datos por repeticion

| Repeticion: R
| Codigo Producto | Catador | P1 | P2 | P3 | Pn |

Encabezados de como deben de aparecer los datos juntos

| Repeticion | Codigo Producto | Catador | P1 | P2 | P3 | Pn |

'''
from tecnicas.models import SesionSensorial, Calificacion, Escala
from tecnicas.controllers import DatoController, PalabrasController
from .details_controller import DetallesController
from tecnicas.utils import defaultdict_to_dict
from collections import defaultdict
from django.urls import reverse


class DetallesEscalasController(DetallesController):
    def __init__(
        self,
        session: SesionSensorial,
        template: str = "tecnicas/manage_sesions/details-session.html",
        back_url: str = "cata_system:panel_sesiones_escalas",
        home_url: str = "cata_system:index_escalas"
    ):
        super().__init__(
            session=session,
            back_url=back_url,
            home_url=home_url
        )
        self.url_template = template
        self.url_next = "cata_system:monitor_sesion"

    def getContext(self):
        technique = self.session.tecnica

        self.context = {
            "use_technique": technique.tipo_tecnica.nombre_tecnica,
            "session": {
                "session_code": self.session.codigo_sesion,
                "session_name": self.session.nombre_sesion or "Sin nombre asignado",
                "session_date": self.session.fechaCreacion,
                "activated": self.session.activo,
                "session_instructions": technique.instrucciones,
            },
            "technique": {
                "words_style": technique.id_estilo,
                "max_catadores": technique.limite_catadores,
                "max_repetitions": technique.repeticiones_max,
                "current_repetition": technique.repeticion,
            },
        }

        # Definir estado de sesion
        # Se comprueba que ya no se pueda iniciar la repeticion
        self.context["fin_repeticiones"] = technique.repeticion >= technique.repeticiones_max and not self.session.activo

        if self.context["fin_repeticiones"]:
            self.context["session"]["session_status"] = "Recolección de datos finalizada"
        elif self.session.activo:
            self.context["session"]["session_status"] = "Sesión en curso"
        else:
            self.context["session"]["session_status"] = "Listo para iniciar repetición"

        # Datos de la escala usada
        scale: Escala = Escala.objects.get(tecnica=technique)

        self.context["scale"] = {
            "type": scale.id_tipo_escala.nombre_escala,
            "size": scale.longitud
        }

        # Recuperar la palabras de la tecnica
        self.words = PalabrasController.getWordsInTechnique(
            technique)
        self.context["palabras"] = [word.nombre_palabra for word in self.words]

        # Se recuperan las calificaciones
        ratings_for_repetition = []

        ratings = list(Calificacion.objects.filter(
            id_tecnica=technique))

        if not ratings:
            self.context["calificaciones"] = ratings_for_repetition
            self.context["existen_calificaciones"] = False
            return self.context

        data = DatoController.getWordValuesForConvecional(
            ratings=ratings, technique=technique)

        ratings_for_repetition = defaultdict(
            lambda: defaultdict(lambda: defaultdict(list)))

        for item in data:
            user = item["usuario_catador"]
            rep = item["repeticion"]
            prod = item["producto_code"]

            ratings_for_repetition[rep][user][prod].append({
                "nombre_palabra": item["nombre_palabra"],
                "dato_valor": item["dato_valor"]
            })

        self.context["calificaciones"] = defaultdict_to_dict(
            ratings_for_repetition)
        self.context["existen_calificaciones"] = True

        return self.context
