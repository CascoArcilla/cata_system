from ..models import Catador, SesionSensorial, Orden, Participacion, Producto, EsAtributo, Calificacion, Vocabulario, EsVocabulario
from ..utils import controller_error, shuffleArray
from django.db import transaction


class MainTesterFormController():
    tester: Catador
    session: SesionSensorial
    order: Orden | dict

    def __init__(self, code_session: str, user_tester: str):
        try:
            self.tester = Catador.objects.get(usuarioCatador=user_tester)
            self.session = SesionSensorial.objects.get(
                codigo_sesion=code_session)
        except (Catador.DoesNotExist, SesionSensorial.DoesNotExist):
            return controller_error("Parámetros inexistentes")

    def assignOrder(self):
        with transaction.atomic():
            orders_without_tester = Orden.objects.select_for_update().filter(
                id_tecnica=self.session.tecnica, id_catador=None)

            if not len(orders_without_tester):
                return controller_error("Las ordenes se han acabado")

            shuffle_orders = shuffleArray(orders_without_tester)
            self.order_to_assign = shuffle_orders.pop()

            self.order_to_assign.id_catador = self.tester
            self.order_to_assign.save()

            return self.order_to_assign

    def checkAssignOrder(self):
        if not self.tester or not self.session:
            return controller_error("Atributos no establecidos")

        try:
            res_order = Orden.objects.get(
                id_tecnica=self.session.tecnica, id_catador=self.tester)
            self.order = res_order
            return self.order
        except Orden.DoesNotExist:
            return controller_error("Catador sin orden")

    def endedToFalseAndActiveTester(self, id_participation: int):
        try:
            self.participation = Participacion.objects.get(id=id_participation)
            self.participation.finalizado = False
            self.participation.activo = True
            self.participation.save()
            return self.participation
        except Participacion.DoesNotExist:
            return controller_error("No se ha encontrado la participación")

    def isEndedSession(self, id_participation: int):
        if not self.order or not id_participation:
            return controller_error("Se requieren datos para comprobar la finalización")

        try:
            self.participation = Participacion.objects.get(id=id_participation)

            if self.participation.finalizado:
                num_products = Producto.objects.filter(
                    id_tecnica=self.session.tecnica).count()

                style_words = self.session.tecnica.id_estilo

                num_words: int

                if style_words.nombre_estilo == "atributos":
                    e_atribues = EsAtributo.objects.get(
                        id_tecnica=self.session.tecnica)
                    num_words = e_atribues.palabras.count()
                elif style_words.nombre_estilo == "vocabulario":
                    e_vocabulary = EsVocabulario.objects.get(
                        id_tecnica=self.session.tecnica)
                    num_words = e_vocabulary.id_vocabulario.palabras.count()

                num_ratings_now = Calificacion.objects.filter(
                    id_tecnica=self.session.tecnica, id_catador=self.tester).count()

                num_ratings_max_by_tester = num_products * num_words

                return not num_ratings_now <= num_ratings_max_by_tester
            else:
                return self.participation.finalizado
        except Participacion.DoesNotExist:
            return controller_error("No se ha encontrado la participación")
