from django.http import HttpRequest
from django.shortcuts import render
from tecnicas.utils import general_error
from .main_general import get_context_main, post_main


def mainSort(req: HttpRequest):
    template = "tecnicas/mains_panels/main-panel-sort.html"
    filters = {"tecnica__tipo_tecnica__nombre_tecnica": "sort"}

    if req.method == "GET":
        context = get_context_main(
            req,
            more_filter=filters,
            name_technique="sort"
        )
        return render(req, template, context)

    elif req.method == "POST":
        return post_main(
            req=req,
            current_template=template,
            more_filter=filters,
            name_technique="sort"
        )

    else:
        return general_error(req, "Método no permitido")
