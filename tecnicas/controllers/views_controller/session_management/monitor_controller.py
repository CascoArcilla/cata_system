from tecnicas.models import SesionSensorial


class MonitorController():
    def __init__(self, session: SesionSensorial):
        self.sensorial_session = session

    def updataSession(self):
        self.sensorial_session = SesionSensorial.objects.get(
            codigo_sesion=self.sensorial_session.codigo_sesion)
