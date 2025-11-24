from .details_controller import DetallesController
from tecnicas.models import SesionSensorial


class DetallesSortController(DetallesController):
    def __init__(self, session: SesionSensorial):
        super().__init__(session)
        self.url_template = "tecnicas/manage_sesions/details-session-sort.html"
        self.url_next = "cata_system:monitor_sesion"

    def getContext(self):
        technique = self.session.tecnica

        finished = False
        status = ""

        if technique.repeticion < technique.repeticiones_max and not self.session.activo:
            status = "En espera para iniciar la sesión"
        elif technique.repeticion >= technique.repeticiones_max and not self.session.activo:
            status = "Esta sesión ha sido finalizada"
            finished = True
        else:
            status = "La sesión está en progreso"

        self.context = {
            "sesion": self.session,
            "technique": technique,
            "status": status,
            "finished": finished
        }

        return self.context
