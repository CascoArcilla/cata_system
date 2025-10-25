from ...models import Orden, Posicion, Producto, Tecnica
from ...utils import controller_error
from django.db import DatabaseError


class OrdenesController():
    products: list[Producto]
    technique: Tecnica
    raw_list_orders: list[dict]
    orders: list[Orden]
    positions: list[Posicion]

    def __init__(self, raw_orders: list[dict], list_products: list[Producto], technique: Tecnica):
        self.products = list_products
        self.technique = technique
        self.raw_list_orders = raw_orders

    def serRawOrders(self, new_raw_orders: list[dict]):
        self.raw_list_orders = new_raw_orders

    def setOrdersToSave(self):
        self.orders = []
        for raw in self.raw_list_orders:
            self.orders.append(Orden(id_tecnica=self.technique))

    def saveOrders(self):
        if not self.orders:
            return controller_error("No se han establecido las órdenes para guardar")
        try:
            for order in self.orders:
                order.save()
            return self.orders
        except DatabaseError as error:
            return controller_error("Error al guardar las ordenes")

    def setPositions(self):
        codes_ids_products = {}
        for product in self.products:
            codes_ids_products[product.codigoProducto] = product.id
        codes_expect = list(codes_ids_products.keys())

        if len(self.orders) != len(self.raw_list_orders):
            return controller_error("El número de ordenes guardados no coinciden con los recibidos")

        self.positions = []
        for index, order in enumerate(self.raw_list_orders):
            received_codes_order = list(order.keys())

            if set(received_codes_order) != set(codes_expect):
                return controller_error("Las ordenes mandadas no contienen los productos esperados")

            for name, position_index in order.items():
                list_product_use = [product for product in self.products
                                    if product.codigoProducto == name]

                if len(list_product_use) != 1:
                    return controller_error("No pueden existir dos productos que ocupen la misma posición de un orden")

                product_use = list_product_use[0]
                new_position = Posicion(
                    id_producto=product_use,
                    id_orden=self.orders[index],
                    posicion=position_index
                )
                self.positions.append(new_position)
        return self.positions

    def savePositions(self):
        if not self.positions:
            return controller_error("No se han establecido posiciones para guarguar")
        try:
            for position in self.positions:
                position.save()
            return self.positions
        except DatabaseError as error:
            return controller_error("Error al guardar las posiciones")

    @staticmethod
    def getOrderById(id: int):
        try:
            order = Orden.objects.get(id=id)
            return order
        except Orden.DoesNotExist:
            return controller_error("No existe orden")
