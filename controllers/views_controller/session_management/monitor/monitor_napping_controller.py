from tecnicas.models import SesionSensorial
from tecnicas.models import Participacion, TecnicaModalidad
from .monitor_controller import MonitorController


class MonitorNappingController(MonitorController):
    def __init__(
        self,
        session: SesionSensorial,
        url_home: str = "cata_system:index"
    ):
        super().__init__(session=session, url_home=url_home)
        self.url_view = "tecnicas/manage_sesions/monitor-sesion.html"
        self.previus_view = "cata_system:detalles_sesion"

    def checkAllFinish(self) -> (bool, str):
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

    def finishSession(self):
        technique = self.sensorial_session.tecnica
        technique.repeticion = 1
        technique.save()
        self.sensorial_session.activo = False
        self.sensorial_session.save()
        return self.sensorial_session
