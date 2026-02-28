from django.db.models import F
from tecnicas.models import SesionSensorial, Calificacion, ValorBooleano
from controllers import PalabrasController
from utils import defaultdict_to_dict
from .details_controller import DetallesController
from collections import defaultdict


class DetallesCATAController(DetallesController):
    def __init__(
        self,
        session: SesionSensorial,
        back_url: str = "cata_system:panel_sesiones_cata",
        home_url: str = "cata_system:index_cata"
    ):
        super().__init__(
            session=session,
            back_url=back_url,
            home_url=home_url
        )
        self.url_template = "manage_sesions/details-session-cata.html"
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

        # Establer estado
        if technique.repeticion == 0:
            self.context["session"]["session_status"] = "Listo para iniciar"
        elif technique.repeticion == 1 and self.session.activo:
            self.context["session"]["session_status"] = "Sesión en curso"
        elif technique.repeticion == 1 and not self.session.activo:
            self.context["session"]["session_status"] = "Recolección de datos finalizada"
        else:
            self.context["session"]["session_status"] = "No se puede establecer el estado"

        # Recuperar palabras
        self.words = PalabrasController.getWordsInTechnique(
            self.session.tecnica)
        self.context["palabras"] = [word.nombre_palabra for word in self.words]

        # Intentar recuperar las calificaciones
        ratings_for_repetition = []

        ratings = list(Calificacion.objects.filter(
            id_tecnica=technique))

        if not ratings:
            self.context["calificaciones"] = ratings_for_repetition
            self.context["existen_calificaciones"] = False
            return self.context

        data = (
            ValorBooleano.objects
            .filter(id_dato__id_calificacion__in=ratings)
            .values(
                nombre_palabra=F("id_dato__id_palabra__nombre_palabra"),
                repeticion=F("id_dato__id_calificacion__num_repeticion"),
                producto_code=F(
                    "id_dato__id_calificacion__id_producto__codigoProducto"),
                usuario_catador=F(
                    "id_dato__id_calificacion__id_catador__user__username"),
                dato_valor=F("valor")
            )
        )

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

        # Se comprueba que ya no se pueda iniciar la repeticion
        self.context["fin_repeticiones"] = technique.repeticion >= technique.repeticiones_max and not self.session.activo
        return self.context
