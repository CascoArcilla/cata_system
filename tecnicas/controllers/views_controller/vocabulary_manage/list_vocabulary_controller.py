from django.shortcuts import render
from django.http import HttpRequest
from django.core.paginator import Paginator, PageNotAnInteger
from tecnicas.models import Vocabulario
from tecnicas.utils import controller_error


class ListVocabularyController():
    current_url = "tecnicas/manage_vocabulary/list-vocabulary.html"

    def __init__(self):
        pass

    def controllGet(self, request: HttpRequest, page: int):
        context = {}

        info_element_page = self.getVocabularys(page)

        if isinstance(info_element_page, dict):
            context["error"] = info_element_page["error"]
            return render(request, self.current_url, context)

        (vocabularies_in_page, is_last_page, current_page) = info_element_page

        context["vocabularies"] = vocabularies_in_page
        context["last_page"] = is_last_page
        context["num_page"] = current_page

        return render(request, self.current_url, context)

    def getVocabularys(self, num_page: int):
        elements_by_page = 6

        queryset = Vocabulario.objects.all().order_by('-creado')

        paginator = Paginator(queryset, elements_by_page)
        try:
            vocabularies_in_page = paginator.page(num_page)
        except PageNotAnInteger:
            return controller_error("índice inválido")

        if not vocabularies_in_page.object_list:
            return controller_error("Sin registros de Participaciones")

        current_page = vocabularies_in_page.number
        is_last_page = not current_page < paginator.num_pages

        return (vocabularies_in_page, is_last_page, current_page)
