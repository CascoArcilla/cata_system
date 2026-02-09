from tecnicas.models import Dato, DatoHedonico, Participacion, Producto, SesionSensorial
from tecnicas.controllers import PalabrasController
from .monitor_controller import MonitorController


class MonitorIdealController(MonitorController):
    def __init__(self, session: SesionSensorial):
        super().__init__(session)
        self.url_view = "tecnicas/manage_sesions/monitor-sesion.html"
        self.previus_view = "cata_system:detalles_sesion"

    def checkAllFinish(self) -> tuple[bool, str]:
        num_testers = Participacion.objects.filter(
            tecnica=self.sensorial_session.tecnica).count()

        num_products = Producto.objects.filter(
            id_tecnica=self.sensorial_session.tecnica).count()

        num_words = len(
            PalabrasController.getWordsInTechnique(self.sensorial_session.tecnica))

        end_phase1 = self.endAllPhase1(num_products, num_words, num_testers)
        if not end_phase1[0]:
            return (False, "Aun no se han registrado todos los datos de la fase 1")

        end_phase2 = self.endAllPhase2(num_products, num_testers)
        if not end_phase2[0]:
            return (False, "Aun no se han registrado todos los datos de la fase 2")

        return (True, "Todos los catadores han finalizado su evaluación")

    def endAllPhase1(self, num_products: int, num_words: int, num_testers: int):
        # ////////////////////////////////////////////////////////////// #
        # datos totales por sesion de escala intensidad como escala ideal = (numero_de_palabras * numero_de_productos) * numero_de_catadores
        # ////////////////////////////////////////////////////////////// #
        expected_data_intensity_ideal = num_products * num_words * num_testers

        current_data_intensity = Dato.objects.filter(
            id_calificacion__id_tecnica=self.sensorial_session.tecnica,
            id_calificacion__num_repeticion=1,
            id_calificacion__calificacion_escala__escala__id_tipo_escala__nombre_escala="estructurada"
        ).count()

        current_data_ideal = Dato.objects.filter(
            id_calificacion__id_tecnica=self.sensorial_session.tecnica,
            id_calificacion__num_repeticion=1,
            id_calificacion__calificacion_escala__escala__id_tipo_escala__nombre_escala="ideal"
        ).count()

        is_end = (current_data_intensity == current_data_ideal ==
                  expected_data_intensity_ideal)

        result = tuple()

        if is_end:
            result = (True, "Fase 1 completada")
        else:
            result = (False, "Fase 1 no completada")

        return result

    def endAllPhase2(self, num_products: int, num_testers: int):
        # ////////////////////////////////////////////////////////////// #
        # datos totales por sesion de escala preferencia = numero_de_productos * numero_de_catadores
        # ////////////////////////////////////////////////////////////// #
        expected_data_preference = num_products * num_testers

        current_data_preference = DatoHedonico.objects.filter(
            calificacion__id_tecnica=self.sensorial_session.tecnica,
            calificacion__num_repeticion=1,
        ).count()

        is_end = (current_data_preference == expected_data_preference)

        result = tuple()

        if is_end:
            result = (True, "Fase 2 completada")
        else:
            result = (False, "Fase 2 no completada")

        return result
