from tecnicas.models import Dato, Participacion, Catador, ListaPalabras, Producto
from tecnicas.controllers import SesionController
from .monitor_controller import MonitorController


class MonitorPFController(MonitorController):
    def __init__(self, session: SesionController):
        super().__init__(session)
        self.url_view = "tecnicas/manage_sesions/monitor-sesion.html"
        self.previus_view = "cata_system:detalles_sesion"

    def checkAllFinish(self):
        rep = self.sensorial_session.tecnica.repeticion

        finish_data = ()

        if rep == 1 or rep == 2:
            finish_data = self.checkFinishFirstPhase()
        elif rep >= 3:
            finish_data = self.checkFinishRepetition()

        return finish_data

    def checkFinishFirstPhase(self):
        num_paricipations = Participacion.objects.filter(
            tecnica=self.sensorial_session.tecnica).count()
        if num_paricipations < self.sensorial_session.tecnica.limite_catadores:
            return (False, "No se ha alcanzado el número máximo de catadores")

        unfinished_participations = Participacion.objects.filter(
            tecnica=self.sensorial_session.tecnica, finalizado=False).count()
        if unfinished_participations:
            return (False, "No todos los catadores han finalizado su evaluación")

        return (True, "Puedes finalizar la sesión")

    def checkFinishRepetition(self) -> tuple[bool, str]:
        technique = self.sensorial_session.tecnica

        # Revisar numero de catadores sea alcanzado
        all_participations = list(
            Participacion.objects.filter(tecnica=technique))
        if len(all_participations) < technique.limite_catadores:
            return (False, "No se ha alcanzado el número máximo de Catadores")

        # Revisar que cada catador haya terminado de calificar sus palabras
        for particiapation in all_participations:
            expected_ratings_repetition = self.getExpectedRatings(
                tester=particiapation.catador)

            num_ratings_now = Dato.objects.filter(
                id_calificacion__num_repeticion=technique.repeticion,
                id_calificacion__id_catador=particiapation.catador,
                id_calificacion__id_tecnica=technique
            ).count()

            if num_ratings_now < expected_ratings_repetition:
                return (False, "No todos los catadores han finalizado su evaluación")

        return (True, "Puedes finalizar la sesión")

    def getExpectedRatings(self, tester: Catador):
        num_words = ListaPalabras.objects.get(
            tecnica=self.sensorial_session.tecnica,
            catador=tester,
            es_final=True
        ).palabras.all().count()

        num_products = Producto.objects.filter(
            id_tecnica=self.sensorial_session.tecnica).count()

        return num_products * num_words
