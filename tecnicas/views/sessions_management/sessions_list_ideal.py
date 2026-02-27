from django.http import HttpRequest, JsonResponse
from .sessions_list import get_sessions_list


def sesionsListIdeal(req: HttpRequest, page: int):
    template = "tecnicas/list_sessions/sessions-ideal.html"
    filters = {"tecnica__tipo_tecnica__nombre_tecnica": "perfil_ideal"}
    url_home = req.session.get("sensorial_url_main")

    if req.method == "GET":
        return get_sessions_list(
            req=req, page=page, filters=filters, template=template, url_home=url_home
        )
    else:
        return JsonResponse({"message": "Método no permitido"})
