from django.db import DatabaseError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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

    @staticmethod
    def getSessionsSavesByCretor(user_name: str, page: int):
        elements_by_page = 9

        try:
            creator = Presentador.objects.get(nombre_usuario=user_name)
        except Presentador.DoesNotExist:
            return controller_error("presentador invalido")

        try:
            queryset = SesionSensorial.objects.select_related(
                "tecnica",
                "tecnica__tipo_tecnica",
                "tecnica__id_estilo"
            ).only(
                "codigo_sesion",
                "nombre_sesion",
                "fechaCreacion",
                "tecnica__tipo_tecnica__nombre_tecnica",
                "tecnica__id_estilo__nombre_estilo"
            )

            paginator = Paginator(queryset, elements_by_page)
            sessions_in_page = paginator.get_page(page)

            return sessions_in_page
        except PageNotAnInteger:
            return controller_error("indice invalido")
        except EmptyPage:
            return controller_error("sin registros de sessiones")

    @staticmethod
    def getSessionByCodePanelTester(code: str):
        try:
            session = SesionSensorial.objects.select_related(
                "tecnica",
                "tecnica__tipo_tecnica",
                "tecnica__id_estilo"
            ).only(
                "codigo_sesion",
                "nombre_sesion",
                "tecnica__repecion",
                "tecnica__instrucciones",
                "tecnica__tipo_tecnica__nombre_tecnica",
                "tecnica__id_estilo__nombre_estilo"
            ).get(codigo_sesion=code)

            return session
        except SesionSensorial.DoesNotExist:
            return controller_error("La sesión ya no existe")

    @staticmethod
    def getNumberSessionsByCreator(user_name: str):
        try:
            creator = Presentador.objects.get(nombre_usuario=user_name)

            number_sessions = SesionSensorial.objects.filter(
                creadoPor=creator).count()

            return number_sessions/9
        except Presentador.DoesNotExist:
            return controller_error("presentador invalido")
