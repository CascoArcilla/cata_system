from django.db import DatabaseError
from ..models import Tecnica, Presentador, SesionSensorial
from ..utils import controller_error


class SesionController():
    def __init__(self, name_session: str, technique: Tecnica, creator: Presentador):
        self.name_session = name_session or None
        self.technique = technique or None
        self.presenter = creator or None

    def setData(self, name_session: str, technique: Tecnica, creator: Presentador):
        self.name_session = name_session
        self.technique = technique
        self.presenter = creator

    def setSession(self):
        if not self.presenter:
            return controller_error("se requiere presentador para crear sesion")
        elif not self.technique:
            return controller_error("se requiere tecnica para crear sesion")

        self.sensorial_session = SesionSensorial(
            tecnica=self.technique,
            creadoPor=self.presenter,
        )

        if self.name_session != "":
            self.sensorial_session.nombre_sesion = self.name_session

        return self.sensorial_session

    def saveSession(self):
        if not self.sensorial_session:
            return controller_error("no se ha definido la sesion a guardar")

        try:
            self.sensorial_session.save()
            return self.sensorial_session
        except DatabaseError as error:
            return controller_error("Error al crear la session sensorial")
