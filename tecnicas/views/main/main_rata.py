from django.http import HttpRequest
from django.shortcuts import render
from tecnicas.utils import general_error
from .main_general import get_context_main, post_main


def mainRata(req: HttpRequest):
    template = "tecnicas/mains_panels/main-panel-rata.html"
    filters = {"tecnica__tipo_tecnica__nombre_tecnica": "rata"}

    if req.method == "GET":
        context = get_context_main(
            req,
            more_filter=filters,
            name_technique="rata"
        )

        return render(req, template, context=context)

    elif req.method == "POST":
        return post_main(
            req=req,
            current_template=template,
            more_filter=filters,
            name_technique="rata"
        )
    else:
        general_error("Método no permitido")
