from django.core.exceptions import ValidationError
from collections import defaultdict
from tecnicas.models import Calificacion, Tecnica, Posicion, Producto, Catador
from tecnicas.utils import controller_error, getId


class CalificacionController():
    def __init__(self, product: Producto | int, technique: Tecnica | int, tester: Catador | int):
        technique = Tecnica.objects.only(
            "repeticion").get(id=getId(technique))

        atributes = {
            "num_repeticion": technique.repeticion,
            "id_tecnica": technique,
            "id_producto_id": getId(product),
            "id_catador_id": getId(tester),
        }

        (self.rating, created) = Calificacion.objects.get_or_create(**atributes)

    @staticmethod
    def getRatingsByTechnique(technique: Tecnica):
        repetition = technique.repeticion
        ratings = list(Calificacion.objects.filter(id_tecnica=technique, num_repeticion=repetition))
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
    def checkPositionWithoutRating(
            positions: list[Posicion] = None,
            user_cata: Catador | str = None,
            repetition: int = None,
            technique: Tecnica | int = None,
            num_words: int = None):
        end_rating = False

        # Obtener lista con codigos de productos
        check_products = [
            position.id_producto.codigoProducto for position in positions]

        filters = {
            "num_repeticion": repetition,
            "id_tecnica": getId(technique)
        }

        if isinstance(user_cata, Catador):
            filters["id_catador"] = user_cata
        else:
            filters["id_catador"] = Catador.objects.get(
                user__username=user_cata)

        ratings = list(Calificacion.objects.filter(**filters).select_related(
            "id_producto",
            "id_tecnica",
            "id_catador",
        ))

        # Si no hay calificaciones regresar las posiciones
        if len(ratings) == 0:
            return (positions, end_rating)

        rating_products = [
            rating.id_producto.codigoProducto for rating in ratings]

        for index, rating in enumerate(ratings):
            data_rating = rating.dato_calificacion.all()

            if len(data_rating) < num_words or len(data_rating) == 0:
                return (positions[index], end_rating)

        next_product = list(set(check_products) - set(rating_products))
        if len(next_product) != 0:
            next_position = [
                position for position in positions if position.id_producto.codigoProducto == next_product[0]][0]
            return (next_position, end_rating)
        else:
            end_rating = True
            return (positions[-1], end_rating)
