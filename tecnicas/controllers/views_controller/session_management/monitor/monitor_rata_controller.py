from tecnicas.models import Dato, Participacion
from tecnicas.controllers import SesionController
from .monitor_controller import MonitorController


class MonitorRATAController(MonitorController):
    def __init__(self, session: SesionController):
        super().__init__(session)
        self.url_view = "tecnicas/manage_sesions/monitor-sesion.html"
        self.previus_view = "cata_system:detalles_sesion"

    def checkAllFinish(self):
        technique = self.sensorial_session.tecnica

        expected_ratings_repetition = self.getExpectedRatings()

        all_participations = list(
            Participacion.objects.filter(tecnica=technique))

        if len(all_participations) == 0:
            return (False, "No hay catadores en la sesión, deben participar al menos un Catador")

        for particiapation in all_participations:
            num_ratings_now = Dato.objects.filter(
                id_calificacion__num_repeticion=technique.repeticion,
                id_calificacion__id_catador=particiapation.catador,
                id_calificacion__id_tecnica=technique
            ).count()

            if num_ratings_now < expected_ratings_repetition:
                return (False, "No todos los catadores han finalizado su evaluación")

        return (True, "Puedes finalizar la sesión")
