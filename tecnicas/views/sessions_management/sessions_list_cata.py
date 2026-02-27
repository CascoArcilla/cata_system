from django.http import HttpRequest, JsonResponse
from .sessions_list import get_sessions_list


def sesionsListCata(req: HttpRequest, page: int):
    template = "tecnicas/list_sessions/sessions-cata.html"
    filters = {"tecnica__tipo_tecnica__nombre_tecnica": "cata"}
    url_home = req.session.get("session_url_home")

    if req.method == "GET":
        return get_sessions_list(
            req=req, page=page, filters=filters, template=template, url_home=url_home
        )
    else:
        return JsonResponse({"message": "Método no permitido"})
