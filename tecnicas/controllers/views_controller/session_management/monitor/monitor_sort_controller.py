from tecnicas.models import SesionSensorial
from tecnicas.models import Participacion
from .monitor_controller import MonitorController


class MonitorSortController(MonitorController):
    def __init__(self, session: SesionSensorial):
        super().__init__(session)
        self.url_view = "tecnicas/manage_sesions/monitor-session-sort.html"
        self.previus_view = "cata_system:detalles_sesion"

    def checkAllFinish(self):
        technique = self.sensorial_session.tecnica

        num_participations = Participacion.objects.filter(
            tecnica=technique).count()

        if num_participations < technique.limite_catadores:
            return (False, "No se ha alcanzado el número máximo de catadores")

        unfinished_participations = Participacion.objects.filter(
            tecnica=technique, finalizado=False).count()

        if unfinished_participations > 0:
            return (False, "No todos los catadores han finalizado su evaluación")

        return (True, "Puedes finalizar la sesión")