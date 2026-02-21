from utils import controller_error
from tecnicas.models import Orden, Posicion


class PosicionController():
    @staticmethod
    def getPostionsInOrder(order: Orden = None, id_order: id = None):
        if order is not None:
            positions = list(Posicion.objects.filter(id_orden=order))
            if not positions:
                return controller_error("No existe orden")
            return positions

        if id_order is not None:
            positions = list(Posicion.objects.filter(id_orden_id=id_order))
            if not positions:
                return controller_error("No existe orden")
            return positions

        return controller_error("No se define búsqueda")
