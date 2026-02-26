from django.http import HttpRequest, JsonResponse
from .sessions_list import get_sessions_list


def sesionsListRata(req: HttpRequest, page: int):
    template = "tecnicas/list_sessions/sessions-rata.html"
    filters = {"tecnica__tipo_tecnica__nombre_tecnica": "rata"}

    if req.method == "GET":
        return get_sessions_list(
            req=req, page=page, filters=filters, template=template
        )
    else:
        return JsonResponse({"message": "Método no permitido"})
