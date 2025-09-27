from ...models import Calificacion, Tecnica, Posicion, Producto, Catador
from ...utils import controller_error
from collections import defaultdict


class CalificacionController():
    @staticmethod
    def getRatingsByTechnique(technique: Tecnica):
        repetition = technique.repecion

        if not repetition:
            return {"error": "sin datos calficados aun"}

        data_rating = {}

        for i in range(repetition):
            response_data = Calificacion.objects.filter(
                id_tecnica=technique, num_repeticion=i+1)
            data_rating[f"repeticion_{i+1}"] = response_data

        return data_rating

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
            filters["id_catador__usuarioCatador"] = user_tester

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
            rating_of_product = ratings_dict.get(product.id, [])

            if rating_of_product < num_words or len(rating_of_product) == 0:
                return positions[index]

        return controller_error("Sin productos por calificar")
