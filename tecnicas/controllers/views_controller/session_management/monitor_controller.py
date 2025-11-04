from tecnicas.models import SesionSensorial


class MonitorController():
    def __init__(self, session: SesionSensorial):
        self.sensorial_session = session
