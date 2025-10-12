from ...models import Calificacion, Dato, Palabra, ValorDecimal, ValorBooleano, Tecnica
from ...utils import controller_error, getId
from django.core.exceptions import ValidationError
from django.db.models import F


class DatoController():
    def __init__(self, word: Palabra | int, rating: Calificacion | int, value_rating: int | bool):
        atributes = {
            "id_palabra_id": getId(word),
            "id_calificacion_id": getId(rating)
        }

        self.data = Dato(**atributes)
        self.value_data = ValorDecimal(valor=value_rating)

    def setRating(self, new_rating: Calificacion):
        try:
            self.data.id_calificacion = new_rating
            return self.data.id_calificacion
        except ValidationError as e:
            return controller_error(e.message)

    def validateRating(self):
        try:
            self.data.full_clean()
            return self.data
        except ValidationError as e:
            return controller_error(e.message)

    def saveData(self):
        try:
            self.data.save()
            return self.data
        except ValidationError as e:
            return controller_error(e.message)

    def setInstanceValue(self):
        technique = self.data.id_calificacion.id_tecnica

        if technique.tipo_tecnica == "cata":
            self.value_data = ValorBooleano(
                id_dato=self.data,
                valor=self.value_data.valor
            )
        else:
            self.value_data = ValorDecimal(
                id_dato=self.data,
                valor=self.value_data.valor
            )

        return self.value_data

    def saveValue(self):
        try:
            self.value_data.save()
            return self.value_data
        except ValidationError as e:
            return controller_error(e.message)

    @staticmethod
    def getRerecordedData(ratings: list[Calificacion]):
        '''
        Get Datos' registers for each Calificacion.
        Datos' registers no contain the value of rating.
        '''
        if not ratings:
            return []

        ids_ratings = [rat.id for rat in ratings]

        recoreded_data = list(Dato.objects.filter(
            id_calificacion_id__in=ids_ratings))

        return recoreded_data

    @staticmethod
    def getWordValuesForConvecional(technique: Tecnica, ratings: list[Calificacion]):
        model = ValorBooleano if technique.tipo_tecnica == "cata" else ValorDecimal

        ids_ratings = [rat.id for rat in ratings]

        result = (
            model.objects
            .filter(id_dato__id_calificacion_id__in=ids_ratings)
            .values(
                nombre_palabra=F("id_dato__id_palabra__nombre_palabra"),
                repeticion=F("id_dato__id_calificacion__num_repeticion"),
                producto_code=F(
                    "id_dato__id_calificacion__id_producto__codigoProducto"),
                usuarioCatador=F(
                    "id_dato__id_calificacion__id_catador__usuarioCatador"),
                dato_valor=F("valor")
            )
        )

        return list(result)
