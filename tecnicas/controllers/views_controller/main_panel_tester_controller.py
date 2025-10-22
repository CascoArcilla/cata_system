from django.core.paginator import Paginator, PageNotAnInteger
from django.db.models import OuterRef, Subquery, BooleanField
from tecnicas.models import Catador, SesionSensorial, Participacion
from tecnicas.utils import controller_error


class MainPanelTesterController():
    def __init__(self):
        pass

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
            .order_by('activo', '-fechaCreacion')
            .distinct()
        )

        paginator = Paginator(queryset, elements_by_page)
        try:
            testers_in_page = paginator.page(page)
        except PageNotAnInteger:
            return controller_error("índice inválido")

        if not testers_in_page.object_list:
            return controller_error("Sin registros de Catadores")

        is_last_page = not testers_in_page.number < paginator.num_pages

        return (testers_in_page, is_last_page)
