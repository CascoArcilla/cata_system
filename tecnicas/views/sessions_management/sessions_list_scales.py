from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from tecnicas.controllers import SesionController
from .sessions_list import get_sessions_list_scales


def sesionsListScales(req: HttpRequest, page: int):
    template = "tecnicas/list_sessions/sessions-scales.html"
    filters = {"tecnica__tipo_tecnica__nombre_tecnica": "escalas"}

    if req.method == "GET":
        return get_sessions_list_scales(
            req=req, page=page, filters=filters, template=template
        )
    else:
        return JsonResponse({"message": "Método no permitido"})
