from ...models import Calificacion, Dato, Palabra
from ...utils import controller_error, getId
from django.core.exceptions import ValidationError


class DatoController():
    def __init__(self, word: Palabra | int, rating: Calificacion | int):
        atributes = {
            "id_palabra_id": getId(word),
            "id_calificacion_id": getId(rating)
        }

        self.data = Dato(**atributes)

    def saveData(self):
        try:
            self.data.full_clean()
            self.data.save()
            return self.data
        except ValidationError as e:
            return controller_error(e.message)

    @staticmethod
    def getRerecordedData(ratings: list[Calificacion]):
        if not ratings:
            return []

        ids_ratings = [rat.id for rat in ratings]

        recoreded_data = list(Dato.objects.filter(
            id_calificacion_id__in=ids_ratings))

        return recoreded_data
