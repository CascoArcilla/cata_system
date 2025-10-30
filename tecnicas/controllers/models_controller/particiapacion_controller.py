from ...models import Participacion, Tecnica, SesionSensorial, Catador
from ...utils import controller_error


class ParticipacionController():
    @staticmethod
    def enterSession(tester: Catador, session: SesionSensorial):
        try:
            participation = Participacion.objects.get(
                catador=tester, tecnica=session.tecnica)
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
    def outAllInSession(session: SesionSensorial | str):
        try:
            if isinstance(session, str):
                use_session = SesionSensorial.objects.get(
                    codigo_sesion=session)
            else:
                use_session = session

            participations = Participacion.objects.filter(
                tecnica=use_session.tecnica)

            if not participations.exists():
                message = "No se encontraron participaciones en la sesión"
                return (False, message)

            participations.update(finalizado=False)

            message = "Participaciones actualizadas a finalizadas"
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
