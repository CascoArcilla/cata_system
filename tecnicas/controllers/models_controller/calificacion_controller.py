from django.core.exceptions import ValidationError
from collections import defaultdict
from tecnicas.models import Calificacion, Tecnica, Posicion, Producto, Catador
from tecnicas.utils import controller_error, getId


class CalificacionController():
    def __init__(self, product: Producto | int, technique: Tecnica | int, tester: Catador | int):
        atributes = {
            "num_repeticion": 0,
            "id_tecnica_id": getId(technique),
            "id_producto_id": getId(product),
            "id_catador_id": getId(tester),
        }

        self.rating = Calificacion(**atributes)

    def validateRating(self):
        try:
            self.rating.clean()
            return self.rating
        except ValidationError as e:
            return controller_error("No es posible validar la calificación")

    def setRepetition(self, repetition: int = None) -> int | dict:
        try:
            if repetition is not None:
                self.rating.num_repeticion = repetition
            else:
                self.rating.num_repeticion = self.rating.id_tecnica.repeticion

            return self.rating.num_repeticion
        except ValidationError as e:
            return controller_error(e)

    def saveRating(self):
        try:
            self.rating.save()
            return self.rating
        except ValidationError as e:
            return controller_error(e)

    @staticmethod
    def getRatingsByTechnique(technique: Tecnica):
        repetition = technique.repeticion

        if not repetition:
            return controller_error("Sin datos calificados aún")

        ratings = list(Calificacion.objects.filter(id_tecnica=technique))

        return ratings

    @staticmethod
    def getRatings(
            technique: Tecnica = None,
            id_technique: int = None,
            repetition: int = None,
            product: Producto = None,
            id_product: int = None,
            tester: Catador = None,
            id_tester: int = None,
            user_tester: str = None,):
        if repetition is None:
            return controller_error("Es necesario especificar la repetición")

        filters = {"num_repeticion": repetition}

        if technique is not None:
            filters["id_tecnica"] = technique
        elif id_technique is not None:
            filters["id_tecnica__id"] = id_technique
        else:
            return controller_error("Es necesario especificar la técnica")

        if product is not None:
            filters["id_producto"] = product
        elif id_product is not None:
            filters["id_producto__id"] = id_product

        if tester is not None:
            filters["id_catador"] = tester
        elif id_tester is not None:
            filters["id_catador__id"] = id_tester
        elif user_tester is not None:
            filters["id_catador__user__username"] = user_tester

        ratings = list(Calificacion.objects.filter(**filters).select_related(
            "id_producto",
            "id_tecnica",
            "id_catador",
        ))

        return ratings

    @staticmethod
    def checkProducsWithoutRating(
            positions: list[Posicion] = None,
            user_cata: str = None,
            repetition: int = None,
            technique: Tecnica = None,
            id_technique: int = None,
            num_words: int = None):
        check_products = [position.id_producto for position in positions]

        filters = {
            "user_tester": user_cata,
            "repetition": repetition
        }

        if technique is not None:
            filters["technique"] = technique
        elif id_technique is not None:
            filters["id_technique"] = id_technique

        ratings = CalificacionController.getRatings(**filters)

        if len(ratings) == 0:
            return positions

        ratings_dict = defaultdict(list)

        for rat in ratings:
            ratings_dict[rat.id_producto.id].append(rat)

        for index, product in enumerate(check_products):
            ratings_of_product = ratings_dict.get(product.id, [])

            if len(ratings_of_product) < num_words or len(ratings_of_product) == 0:
                return positions[index]

        return controller_error("Sin productos por calificar")
