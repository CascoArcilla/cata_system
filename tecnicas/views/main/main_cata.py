from django.http import HttpRequest
from django.shortcuts import render
from tecnicas.utils import general_error
from .main_general import get_context_main, post_main


def mainCata(req: HttpRequest):
    template = "tecnicas/mains_panels/main-panel-cata.html"
    filters = {"tecnica__tipo_tecnica__nombre_tecnica": "cata"}

    if req.method == "GET":
        context = get_context_main(
            req,
            more_filter=filters,
            name_technique="cata"
        )

        return render(req, template, context=context)

    elif req.method == "POST":
        return post_main(
            req=req,
            current_template=template,
            more_filter=filters,
            name_technique="cata"
        )
    else:
        general_error("Método no permitido")
