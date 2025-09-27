from ...models import Calificacion, Dato
from ...utils import controller_error


class DatoController():
    @staticmethod
    def getRerecordedData(ratings: list[Calificacion]):
        if not ratings:
            return []
        
        ids_ratings = [rat.id for rat in ratings]

        recoreded_data = list(Dato.objects.filter(
            id_calificacion_id__in=ids_ratings))
        
        return recoreded_data
