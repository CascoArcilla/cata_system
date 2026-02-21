from django.db import DatabaseError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from tecnicas.models import Tecnica, Presentador, SesionSensorial
from utils import controller_error
from .particiapacion_controller import ParticipacionController


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
            return controller_error("Se requiere presentador para crear sesión")
        elif not self.technique:
            return controller_error("Se requiere técnica para crear sesión")

        self.sensorial_session = SesionSensorial(
            tecnica=self.technique,
            creadoPor=self.presenter,
        )

        if self.name_session != "":
            self.sensorial_session.nombre_sesion = self.name_session

        return self.sensorial_session

    def saveSession(self):
        if not self.sensorial_session:
            return controller_error("No se ha definido la sesión a guardar")

        try:
            self.sensorial_session.save()
            return self.sensorial_session
        except DatabaseError as error:
            return controller_error("Error al crear la sesión sensorial")

    @staticmethod
    def getSessionsByCretor(user_name: str, page: int, filters: dict = None):
        elements_by_page = 6

        if filters is None:
            try:
                creator = Presentador.objects.get(user__username=user_name)
            except Presentador.DoesNotExist:
                return controller_error("Presentador invalido")
            filters = { "creadoPor":creator }

        queryset = (
            SesionSensorial.objects
            .filter(**filters)
            .select_related(
                "tecnica",
                "tecnica__tipo_tecnica",
                "tecnica__id_estilo"
            )
            .only(
                "codigo_sesion",
                "nombre_sesion",
                "fechaCreacion",
                "activo",
                "tecnica__tipo_tecnica__nombre_tecnica",
                "tecnica__tipo_tecnica__descripcion",
                "tecnica__id_estilo__nombre_estilo"
            )
            .order_by("-activo", "-fechaCreacion")
        )

        paginator = Paginator(queryset, elements_by_page)
        try:
            sessions_in_page = paginator.page(page)
        except PageNotAnInteger:
            return controller_error("índice inválido")
        except EmptyPage:
            return controller_error("Sin registros en este índice")

        if not sessions_in_page.object_list:
            return controller_error("Sin registros de sesiones")

        current_page = sessions_in_page.number
        is_last_page = not current_page < paginator.num_pages

        return (sessions_in_page, is_last_page, current_page)