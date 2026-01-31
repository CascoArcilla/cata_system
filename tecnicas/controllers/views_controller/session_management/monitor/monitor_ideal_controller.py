from tecnicas.models import Dato, Participacion
from tecnicas.controllers import SesionController
from .monitor_controller import MonitorController


class MonitorIdealController(MonitorController):
    def __init__(self, session: SesionController):
        super().__init__(session)
        self.url_view = "tecnicas/manage_sesions/monitor-sesion.html"
        self.previus_view = "cata_system:detalles_sesion"

    def checkAllFinish(self):
        return (False, "No todos los catadores han finalizado su evaluación")
