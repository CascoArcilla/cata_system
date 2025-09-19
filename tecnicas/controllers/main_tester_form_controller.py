from ..models import Catador, SesionSensorial, Orden
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
        self.checkAssignOrder()
        if isinstance(self.order, Orden):
            return self.order

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
        if not self.tester or self.session:
            return controller_error("Atributos no establecidos")

        try:
            res_order = Orden.objects.get(
                id_tecnica=self.session.tecnica, id_catador=self.tester.id)
            self.order = res_order
        except Orden.DoesNotExist:
            return controller_error("Catador sin orden")
