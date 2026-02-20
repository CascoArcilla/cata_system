from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from tecnicas.models import Catador
from utils import controller_error


class TesterListController():
    def __init__(self, page: int):
        self.num_page = page

    def getContext(self):
        view_context = {"num_page": self.num_page}

        res_tuple = TesterListController.getTestersByPage(page=self.num_page)

        if isinstance(res_tuple, dict):
            view_context["error"] = res_tuple["error"]
            return view_context

        (testers, last_page) = res_tuple

        view_context["testers"] = testers
        view_context["last_page"] = last_page

        return view_context

    @staticmethod
    def getTestersByPage(page: int):
        elements_by_page = 6

        queryset = (
            Catador.objects
            .select_related(
                "user"
            )
            .only(
                "user__first_name",
                "user__last_name",
                "user__username",
                "user__email",
                "genero",
                "telefono",
                "nacimiento"
            )
            .order_by("-user__date_joined")
        )

        paginator = Paginator(queryset, elements_by_page)
        try:
            testers_in_page = paginator.page(page)
        except PageNotAnInteger:
            return controller_error("índice inválido")
        except EmptyPage:
            return controller_error("Sin registros en este índice")

        if not testers_in_page.object_list:
            return controller_error("Sin registros de Catadores")

        is_last_page = not testers_in_page.number < paginator.num_pages

        return (testers_in_page, is_last_page)
