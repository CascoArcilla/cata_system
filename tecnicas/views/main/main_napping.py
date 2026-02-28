from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from utils import general_error
from .main_general import get_context_main, post_main


def mainNapping(req: HttpRequest):
    template = "tecnicas/mains_panels/main-panel-napping.html"
    filters = {"tecnica__tipo_tecnica__nombre_tecnica": "napping"}

    if req.method == "GET":
        context = get_context_main(
            req,
            more_filter=filters,
            name_technique="napping"
        )
        return render(req, template, context)

    elif req.method == "POST":
        return post_main(
            req=req,
            current_template=template,
            more_filter=filters,
            name_technique="napping"
        )

    else:
        return general_error(req, "Método no permitido")
