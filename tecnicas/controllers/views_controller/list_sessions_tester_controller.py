from django.core.paginator import Paginator, PageNotAnInteger
from django.db.models import OuterRef, Subquery, BooleanField
from tecnicas.models import Catador, SesionSensorial, Participacion
from tecnicas.utils import controller_error


class ListSessionsTesterController():
    def __init__(self):
        pass

    def getContext(self, user: Catador, page: int):
        context_view = {}

        response = ListSessionsTesterController.getSessionByTester(page, user)
        if isinstance(response, dict):
            return response

        (sessions, is_last_page, current_page) = response
        context_view["sessions"] = sessions
        context_view["last_page"] = is_last_page
        context_view["page"] = current_page

        return context_view

    @staticmethod
    def getSessionByTester(page: int, tester: Catador):
        elements_by_page = 6

        base_qs = SesionSensorial.objects.filter(
            tecnica__tecnica_participacion__catador=tester
        )

        participacion_finalizado_subq = Subquery(
            Participacion.objects.filter(
                tecnica=OuterRef('tecnica_id'),
                catador=tester
            ).values('finalizado')[:1],
            output_field=BooleanField()
        )

        participacion_activo_subq = Subquery(
            Participacion.objects.filter(
                tecnica=OuterRef('tecnica_id'),
                catador=tester
            ).values('activo')[:1],
            output_field=BooleanField()
        )

        queryset = (
            base_qs
            .select_related(
                'tecnica',
                'tecnica__tipo_tecnica',
                'tecnica__id_estilo',
            )
            .annotate(
                participacion_finalizado=participacion_finalizado_subq,
                participacion_activo=participacion_activo_subq,
            )
            .order_by('participacion_finalizado', '-activo', '-fechaCreacion')
            .distinct()
        )

        paginator = Paginator(queryset, elements_by_page)
        try:
            sessions_in_page = paginator.page(page)
        except PageNotAnInteger:
            return controller_error("índice inválido")

        if not sessions_in_page.object_list:
            return controller_error("Sin registros de Catadores")

        current_page = sessions_in_page.number
        is_last_page = not current_page < paginator.num_pages

        return (sessions_in_page, is_last_page, current_page)
