from ...models import Participacion, Tecnica
from ...utils import controller_error


class ParticipacionController():
    @staticmethod
    def enterSession(id_participation: int):
        try:
            participation = Participacion.objects.get(id=id_participation)
            participation.finalizado = False
            participation.activo = True
            participation.save()
            return participation
        except Participacion.DoesNotExist:
            return controller_error("No se ha encontrado la participación")
        
    @staticmethod
    def finishSession(id_participation: int):
        try:
            participation = Participacion.objects.get(id=id_participation)
            participation.finalizado = True
            participation.activo = False
            participation.save()
            return participation
        except Participacion.DoesNotExist:
            return controller_error("No se ha encontrado la participación")
        
    @staticmethod
    def outSession(id_participation: int):
        try:
            participation = Participacion.objects.get(id=id_participation)
            participation.activo = False
            participation.save()
            return participation
        except Participacion.DoesNotExist:
            return controller_error("No se ha encontrado la participación")
        
    @staticmethod
    def getParticipationsInTechinique(technique: Tecnica| int):
        filters = {}

        if isinstance(technique, int):
            filters["tecnica_id"] = technique
        else:
            filters["tecnica"] = technique

        participations = list(Participacion.objects.filter(**filters))
        return participations
