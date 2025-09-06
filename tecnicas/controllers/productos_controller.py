from django.db import DatabaseError
from ..utils import controller_error
from ..models import Producto, Tecnica


class ProductosController():
    list_codes: list[str]
    list_product: list[Producto]
    technique: Tecnica

    def __init__(self, codes: list[str], technique: Tecnica):
        for code in codes:
            self.list_codes.append(code)

        self.technique = technique

    def setListCodes(self, codes: list[str]):
        for code in codes:
            self.list_codes.append(code)

    def setTechnique(self, technique: Tecnica):
        self.technique = technique

    def setProductsNoSave(self):
        self.list_product = []
        for code in self.list_codes:
            product = Producto(
                codigoProducto=code,
                id_tecnica=self.technique
            )
            self.list_product.append(product)

    def saveProducts(self):
        if not self.list_product:
            return controller_error("no se han establecido los productos para guardar")

        try:
            self.products_save = Producto.objects.bulk_create(self.list_product)
            return self.products_save
        except DatabaseError as error:
            return controller_error(error)
