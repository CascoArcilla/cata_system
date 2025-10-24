from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from tecnicas.controllers import PanelTagsController


def configurationPanelTags(req: HttpRequest):
    basic_data = req.session.get("form_basic")
    if not basic_data:
        return redirect(reverse('cata_system:panel_configuracion_basic'))

    if req.method == "GET":
        if basic_data["name_tecnica"] == "escalas":
            response = PanelTagsController.controllGetConvencional(
                request=req, data=basic_data)
        else:
            response = redirect(
                reverse("cata_system:seleccion_tecnica") + "?error=Técnica no valida")

        return response
    elif req.method == "POST":
        response = PanelTagsController.controllPostConvencional(
            request=req, data=basic_data)
        return response
    else:
        return JsonResponse({"message": "Método no permitido"})
