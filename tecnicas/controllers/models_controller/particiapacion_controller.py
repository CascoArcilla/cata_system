from ...models import Participacion
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
