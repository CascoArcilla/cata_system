from tecnicas.models import SesionSensorial
from .details_controller import DetallesController


class DetallesPFController(DetallesController):
    def __init__(self, session: SesionSensorial):
        super().__init__(session)
        self.url_template = "tecnicas/manage_sesions/details-session-pf.html"
        self.url_next = "cata_system:monitor_sesion"

    def getContext(self):
        technique = self.session.tecnica

        self.context = {
            "sesion": self.session,
            "use_technique": technique,
            "calificaciones": [],
            "existen_calificaciones": False,
            "tipo_escala": technique.escala_tecnica.id_tipo_escala.nombre_escala,
            "valor_max": technique.escala_tecnica.longitud
        }

        # Definir el estado de la sesion
        rep = technique.repeticion
        activate = self.session.activo

        self.context["estado"] = self.getStatus(rep, activate)

        return self.context

    def getStatus(self, rep: int, activate: bool):
        status = ""

        if rep == 0 and not activate:
            status = "Listo para crear listas iniciales"

        elif rep == 1 and activate:
            status = "En primera fase, creación de listas iniciales"
        elif rep == 1 and not activate:
            status = "Listo para crear listas finales"

        elif rep == 2 and activate:
            status = "En segunda fase, creación de listas finales"
        elif rep == 2 and not activate:
            status = "Listo para calificaciones"

        elif rep > 2 and not activate:
            status = "Listo para calificaciones"
        elif rep > 2 and activate:
            status = "Catadores calificando"

        return status
