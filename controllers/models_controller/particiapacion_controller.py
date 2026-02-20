from django.utils import timezone
from datetime import timedelta
from tecnicas.models import Participacion, Tecnica, SesionSensorial, Catador
from utils import controller_error


class ParticipacionController():
    @staticmethod
    def enterSession(tester: Catador, session: SesionSensorial):
        try:
            participation = Participacion.objects.get(
                catador=tester, tecnica=session.tecnica)
            participation.finalizado = False
            participation.activo = True
            participation.last_activity = timezone.now()
            participation.save()
            return participation
        except Participacion.DoesNotExist:
            return controller_error("No se ha encontrado la participación")

    @staticmethod
    def finishSession(participation: Participacion):
        participation.refresh_from_db()
        participation.finalizado = True
        participation.activo = False
        participation.save()
        return participation

    @staticmethod
    def outSession(tester: Catador, session: SesionSensorial):
        try:
            participation = Participacion.objects.get(
                catador=tester, tecnica=session.tecnica)
            participation.activo = False
            participation.save()
            return participation
        except Participacion.DoesNotExist:
            return controller_error("No se ha encontrado la participación")
    
    @staticmethod
    def updateActivity(tester: Catador, session: SesionSensorial):
        try:
            participation = Participacion.objects.get(
                catador=tester, tecnica=session.tecnica)
            participation.activo = True
            participation.last_activity = timezone.now()
            participation.save(update_fields=['activo', 'last_activity'])
            return participation
        except Participacion.DoesNotExist:
            return controller_error("No se ha encontrado la participación")

    @staticmethod
    def checkStaleParticipations(technique: Tecnica, timeout_seconds: int = 600):
        """
        Checks for participations that have been inactive for longer than timeout_seconds
        and marks them as inactive.
        """
        threshold = timezone.now() - timedelta(seconds=timeout_seconds)
        stale_participations = Participacion.objects.filter(
            tecnica=technique,
            activo=True,
            last_activity__lt=threshold
        )
        
        count = stale_participations.count()
        if count > 0:
            stale_participations.update(activo=False)
            
        return count

    @staticmethod
    def outAllInSession(session: SesionSensorial):
        try:
            participations = Participacion.objects.filter(
                tecnica=session.tecnica)

            participations.update(finalizado=False, activo=False)

            message = "Participaciones actualizadas a finalizadas como falso"
            return (True, message)
        except Exception as e:
            print(f"Error al actualizar las participaciones: {str(e)}")
            return (False, "Error al actualizar las participaciones")

    @staticmethod
    def getParticipationsInTechinique(technique: Tecnica | int):
        filters = {}

        if isinstance(technique, int):
            filters["tecnica_id"] = technique
        else:
            filters["tecnica"] = technique

        return list(Participacion.objects.filter(**filters))
