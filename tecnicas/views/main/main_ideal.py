from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from tecnicas.utils import general_error
from .main_general import get_context_main, post_main


def mainIdeal(req: HttpRequest):
    template = "tecnicas/mains_panels/main-panel-ideal.html"
    filters = {"tecnica__tipo_tecnica__nombre_tecnica": "perfil_ideal"}

    if req.method == "GET":
        context = get_context_main(
            req,
            more_filter=filters,
            name_technique="perfil_ideal"
        )
        return render(req, template, context)

    elif req.method == "POST":
        return post_main(
            req=req,
            current_template=template,
            more_filter=filters,
            name_technique="perfil_ideal"
        )

    else:
        return general_error(req, "Método no permitido")
