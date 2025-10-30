from tecnicas.models import Catador, SesionSensorial, Orden, Participacion, Producto, EsAtributo, Calificacion, EsVocabulario
from ...utils import controller_error, shuffleArray
from django.db import transaction


class MainTesterFormController():
    tester: Catador
    session: SesionSensorial
    order: Orden | dict

    def __init__(self, code_session: str, user_tester: str):
        try:
            self.tester = Catador.objects.get(user__username=user_tester)
            self.session = SesionSensorial.objects.get(
                codigo_sesion=code_session)
        except (Catador.DoesNotExist, SesionSensorial.DoesNotExist):
            return controller_error("Parámetros inexistentes")

    def assignOrder(self):
        with transaction.atomic():
            orders_without_tester = list(Orden.objects.select_for_update().filter(
                id_tecnica=self.session.tecnica, id_catador=None))

            print(orders_without_tester)

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

    def isEndedSession(self, repetition: int):
        try:
            participation = Participacion.objects.get(
                catador=self.tester, tecnica=self.session.tecnica)

            # ////////////////////////////////////////////////////////////// #
            #
            # Si numero_calificaciones_esperadas = num_productos * num_palabras
            # Es igual a numero_calificaciones_actuales en la repetcion R
            # Ha terminado la repeticion
            #
            # ////////////////////////////////////////////////////////////// #

            if participation.finalizado:
                num_products = Producto.objects.filter(
                    id_tecnica=self.session.tecnica).count()

                style_words = self.session.tecnica.id_estilo

                num_words: int

                if style_words.nombre_estilo == "atributos":
                    num_words = EsAtributo.objects.get(
                        id_tecnica=self.session.tecnica).palabras.count()
                elif style_words.nombre_estilo == "vocabulario":
                    num_words = EsVocabulario.objects.get(
                        id_tecnica=self.session.tecnica).id_vocabulario.palabras.count()

                num_ratings_now = Calificacion.objects.filter(
                    id_tecnica=self.session.tecnica, id_catador=self.tester, num_repeticion=repetition).count()

                expected_ratings_repetition = num_products * num_words

                return num_ratings_now >= expected_ratings_repetition
            else:
                return participation.finalizado
        except Participacion.DoesNotExist:
            return controller_error("No se ha encontrado la participación")
