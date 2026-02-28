from django.http import HttpRequest, JsonResponse
from .sessions_list import get_sessions_list


def sesionsListRata(req: HttpRequest, page: int):
    template = "list_sessions/sessions-rata.html"
    filters = {"tecnica__tipo_tecnica__nombre_tecnica": "rata"}
    url_home = req.session.get("session_url_home")

    if req.method == "GET":
        return get_sessions_list(
            req=req, page=page, filters=filters, template=template, url_home=url_home
        )
    else:
        return JsonResponse({"message": "Método no permitido"})
