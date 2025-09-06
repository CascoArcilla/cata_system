from ..models import Orden, Posicion, Producto, Tecnica
from ..utils import controller_error
from django.db import DatabaseError


class OrdenesController():
    products: list[Producto]
    technique: Tecnica
    raw_list_orders: list[list[dict]]
    orders: list[Orden]
    orders_save: list[Orden]
    positions: list[Posicion]

    def __init__(self, raw_orders: list[list[dict]], list_products: list[Producto], technique: Tecnica):
        self.products = list_products
        self.technique = technique
        self.raw_list_orders = raw_orders

    def setOrders(self, new_raw_orders: list[list[dict]] = None):
        self.orders = new_raw_orders or []

        for i in range(len(self.raw_list_orders)):
            self.orders.append(Orden(id_tecnica=self.technique))

    def saveOrders(self):
        if not self.orders:
            return controller_error("no se han establecido las ordenes para guardar")
        try:
            self.orders_save = Orden.objects.bulk_create(self.orders)
            return self.orders_save
        except DatabaseError as error:
            return controller_error(error)

    def setPositions(self):
        codes_ids = [(product.codigoProducto, product.id)
                     for product in self.products]

        codes_expect = [pair[0] for pair in codes_ids]

        if len(self.orders_save) != len(self.raw_list_orders):
            return controller_error("el numero de ordenes guardados no coinciden con los recibidos")

        self.positions = []

        for index, raw_order in enumerate(self.raw_list_orders):
            codes_raw_orders = [next(iter(position.values()))
                                for position in raw_order]

            if not set(codes_raw_orders) == set(codes_expect):
                self.positions = []
                return controller_error("las ordenes mandadas no contienen los productos esperados")

            for data_position in raw_order:
                code = data_position["code"]
                position = data_position["position"]

                locate_code_id = [
                    code_id for code_id in codes_ids if code in code_id]

                if not len(locate_code_id) == 1:
                    return controller_error("no es posible asociar mas de un producto a un modelo posicion")
                else:
                    locate_code_id = locate_code_id[0]

                new_position = Posicion(
                    id_producto=Producto.objects.get(id=locate_code_id[1]),
                    id_orden=self.saveOrders[index],
                    posicion=position,
                )

                self.positions.append(new_position)

        return self.positions

    def savePostions(self):
        if not self.positions:
            return controller_error("no se han establecido posiciones para guargar")
        try:
            self.positions_save = Posicion.objects.bulk_create(self.positions)
            return self.positions_save
        except DatabaseError as error:
            return controller_error(error)
