from tecnicas.models import Calificacion, Dato, Palabra, ValorDecimal, ValorBooleano, Tecnica, Catador
from utils import controller_error, getId
from django.core.exceptions import ValidationError
from django.db.models import F


class DatoController():
    def __init__(self, word: Palabra | int, rating: Calificacion | int, value_rating: int | bool):
        atributes = {
            "id_palabra_id": getId(word),
            "id_calificacion_id": getId(rating)
        }

        self.data = Dato(**atributes)
        self.value_rating = value_rating

    def setRating(self, new_rating: Calificacion):
        """
        Cambia la calificación asociada al dato.\n
        No guarda el dato en la base de datos. \n
        """
        try:
            self.data.id_calificacion = new_rating
            return self.data.id_calificacion
        except ValidationError as e:
            return controller_error(e.message)

    def validateRating(self):
        """
        Valida el dato con los atributos del modelo.
        """
        try:
            self.data.full_clean()
            return self.data
        except ValidationError as e:
            return controller_error(e.message)

    def saveData(self):
        """
        Guarda la instancia de Dato en la base de datos.\n
        Aquí no se guarda el valor del dato.\n
        """
        try:
            self.data.save()
            return self.data
        except ValidationError as e:
            return controller_error(e.message)

    def setValue(self):
        """
        Establece el valor del dato.\n
        Si el tipo de técnica es "cata", se establece el valor como booleano.\n
        Si es escala continua, se divide el valor entre 100 y se redondea.\n
        Si es escala no continua, el valor se usa de forma directa.
        """
        type_technique = self.data.id_calificacion.id_tecnica.tipo_tecnica
        if type_technique == "cata":
            self.value_data = ValorBooleano(valor=self.value_rating)

        else:
            type_scale = self.data.id_calificacion.id_tecnica.escala_tecnica.id_tipo_escala.nombre_escala

            if type_scale == "continua":
                decimal_value = self.value_rating/100
                value_rounded = round(decimal_value)
                self.value_data = ValorDecimal(valor=value_rounded)

            else:
                self.value_data = ValorDecimal(valor=self.value_rating)

        self.value_data.id_dato = self.data
        return self.value_data

    def saveValue(self):
        """
        Guarda la instancia de ValorBooleano o ValorDecimal en la base de datos.
        """
        try:
            self.value_data.save()
            return self.value_data
        except ValidationError as e:
            return controller_error(e.message)

    @staticmethod
    def getRerecordedData(ratings: list[Calificacion]):
        '''
        Obtiene los registros de Dato para cada Calificacion.
        Los registros de Dato no contienen el valor de la calificación.
        '''
        if not ratings:
            return []

        ids_ratings = [rat.id for rat in ratings]

        recoreded_data = list(Dato.objects.filter(
            id_calificacion_id__in=ids_ratings))

        return recoreded_data

    @staticmethod
    def getWordValuesForConvecional(technique: Tecnica, ratings: list[Calificacion]):
        """
        Obtiene los valores de las palabras para una técnica convencional.
        """
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
                usuario_catador=F(
                    "id_dato__id_calificacion__id_catador__user__username"),
                dato_valor=F("valor")
            )
        )

        return list(result)

    @staticmethod
    def getWordValuesPF(technique: Tecnica, ratings: list[Calificacion], tester: Catador):
        """
        Obtiene los valores de las palabras para una técnica de perfil ideal.
        """
        ids_ratings = [rat.id for rat in ratings]

        result = (
            ValorDecimal.objects
            .filter(id_dato__id_calificacion_id__in=ids_ratings, id_dato__id_calificacion__id_catador=tester)
            .values(
                nombre_palabra=F("id_dato__id_palabra__nombre_palabra"),
                repeticion=F("id_dato__id_calificacion__num_repeticion"),
                producto_code=F(
                    "id_dato__id_calificacion__id_producto__codigoProducto"),
                dato_valor=F("valor")
            )
        )

        return list(result)
