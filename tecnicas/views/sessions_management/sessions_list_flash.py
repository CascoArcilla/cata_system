from django.http import HttpRequest, JsonResponse
from .sessions_list import get_sessions_list


def sesionsListFlash(req: HttpRequest, page: int):
    template = "tecnicas/list_sessions/sessions-flash.html"
    filters = {"tecnica__tipo_tecnica__nombre_tecnica": "perfil flash"}

    if req.method == "GET":
        return get_sessions_list(
            req=req, page=page, filters=filters, template=template
        )
    else:
        return JsonResponse({"message": "Método no permitido"})
