from tecnicas.models import SesionSensorial
from tecnicas.controllers import ParticipacionController
from tecnicas.utils import controller_error


class MonitorSesionController():
    def __init__(self, session_code: str):
        self.code_session = session_code

    def monitorView(self):
        try:
            self.sensorial_session = SesionSensorial.objects.select_related(
                "tecnica"
            ).only(
                "nombre_sesion",
                "tecnica__limite_catadores",
            ).get(codigo_sesion=self.code_session)

            self.participations = ParticipacionController.getParticipationsInTechinique(
                self.sensorial_session.tecnica)
        except SesionSensorial.DoesNotExist as error:
            return controller_error("No existe Sesión sensorial")

        context = {
            "session_name": self.sensorial_session.nombre_sesion,
            "max_testers": self.sensorial_session.tecnica.limite_catadores,
            "current_testers": len(self.participations),
            "active_testers": len([part for part in self.participations if part.activo]),
            "participations": self.participations
        }

        return context
