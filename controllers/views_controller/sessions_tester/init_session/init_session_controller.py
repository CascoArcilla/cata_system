from django.db import transaction
from tecnicas.models import Catador, SesionSensorial, Orden, Participacion, Producto, EsAtributo, EsVocabulario, Dato
from utils import controller_error, shuffleArray


class InitSessionController():
    tester: Catador
    session: SesionSensorial
    order: Orden | dict
    current_direction: str
    current_direction = "forms_tester/init_scales_test.html"
    escalas_direction = "cata_system:session_convencional"

    def __init__(self, sensorial_session: SesionSensorial, user_tester: Catador):
        self.tester = user_tester
        self.session = sensorial_session

    def assignOrder(self):
        with transaction.atomic():
            orders_without_tester = list(Orden.objects.select_for_update().filter(
                id_tecnica=self.session.tecnica, id_catador=None))

            if not orders_without_tester:
                return controller_error("Las ordenes se han acabado")

            shuffle_orders = shuffleArray(orders_without_tester)
            self.order_to_assign = shuffle_orders.pop()

            self.order_to_assign.id_catador = self.tester
            self.order_to_assign.save()

            return self.order_to_assign

    def checkAndAssignOrder(self):
        try:
            self.order_to_assign = Orden.objects.get(
                id_tecnica=self.session.tecnica, id_catador=self.tester)
        except Orden.DoesNotExist:
            create = self.assignOrder()
            if isinstance(create, dict):
                return create
        return self.order_to_assign

    def isEndedSession(self):
        try:
            participation = Participacion.objects.get(
                catador=self.tester, tecnica=self.session.tecnica)
            self.session.refresh_from_db()

            # ////////////////////////////////////////////////////////////// #
            #
            # numero_datos_esperadas = num_productos * num_palabras
            # Si numero_datos_esperadas es igual a numero_datos_actuales en la repetcion R
            # Ha terminado la repeticion
            #
            # ////////////////////////////////////////////////////////////// #

            if participation.finalizado:
                num_products = Producto.objects.filter(
                    id_tecnica=self.session.tecnica).count()

                technique = self.session.tecnica
                style_words = technique.id_estilo.nombre_estilo

                num_words: int

                if style_words == "atributos":
                    num_words = EsAtributo.objects.get(
                        id_tecnica=self.session.tecnica).palabras.count()
                elif style_words == "vocabulario":
                    num_words = EsVocabulario.objects.get(
                        id_tecnica=self.session.tecnica).id_vocabulario.palabras.count()

                expected_ratings_repetition = num_products * num_words

                num_ratings_now = Dato.objects.filter(
                    id_calificacion__id_catador=self.tester,
                    id_calificacion__id_tecnica=technique,
                    id_calificacion__num_repeticion=technique.repeticion
                ).count()

                is_end = num_ratings_now >= expected_ratings_repetition

                return is_end
            else:
                return participation.finalizado
        except Participacion.DoesNotExist:
            return controller_error("No se ha encontrado la participación")
