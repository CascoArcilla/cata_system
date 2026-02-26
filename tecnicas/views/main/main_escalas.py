from django.http import HttpRequest
from django.shortcuts import render
from tecnicas.utils import general_error
from .main_general import get_context_main, post_main


def mainEscalas(req: HttpRequest):
    template = "tecnicas/mains_panels/main-panel-escalas.html"
    filters = {"tecnica__tipo_tecnica__nombre_tecnica": "escalas"}

    if req.method == "GET":
        context = get_context_main(
            req,
            more_filter=filters
        )

        context["technique"] = "escalas"

        return render(req, template, context=context)

    elif req.method == "POST":
        return post_main(
            req=req,
            technique="escalas",
            current_template=template,
            more_filter=filters
        )
    else:
        general_error("Método no permitido")
