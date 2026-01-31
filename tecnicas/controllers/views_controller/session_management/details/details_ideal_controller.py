from tecnicas.models import SesionSensorial
from tecnicas.controllers import PalabrasController
from .details_controller import DetallesController

class DetallesIdealController(DetallesController):
    def __init__(self, session: SesionSensorial):
        super().__init__(session)
        self.url_template = "tecnicas/manage_sesions/details-session-ideal.html"
        self.url_next = "cata_system:monitor_sesion"

    def getContext(self):
        technique = self.session.tecnica

        self.context = {
            "use_technique": "Perfil Ideal", # Display name, can be prettier than db name
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

        # Establecer estado
        if technique.repeticion == 0:
            self.context["session"]["session_status"] = "Sesion lista para iniciar"
        elif technique.repeticion == 1 and self.session.activo:
            self.context["session"]["session_status"] = "Sesion en curso"
        elif technique.repeticion == 1 and not self.session.activo:
            self.context["session"]["session_status"] = "Recoleccion de datos finalizada"
        else:
            self.context["session"]["session_status"] = "Estado desconocido"

        # Recuperar palabras
        self.words = PalabrasController.getWordsInTechnique(
            self.session.tecnica)
        self.context["palabras"] = [word.nombre_palabra for word in self.words]
        
        # Calificaciones - Por ahora no implementado
        self.context["existen_calificaciones"] = False
        
        # Se comprueba que ya no se pueda iniciar la repeticion
        self.context["fin_repeticiones"] = technique.repeticion >= technique.repeticiones_max and not self.session.activo

        return self.context
