from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from tecnicas.controllers import PanelTagsController
from tecnicas.utils import deleteDataSession


def configurationPanelTags(req: HttpRequest):
    if not req.session.get("form_basic"):
        deleteDataSession(req)
        return redirect(reverse('cata_system:panel_configuracion_basic') +
                        "?error=datos requeridos no encontrados")

    basic_data = req.session.get("form_basic")

    if req.method == "GET":
        if basic_data["name_tecnica"] == "escalas" or basic_data["name_tecnica"] == "rata":
            response = PanelTagsController.controllGetEscalas(
                request=req, data=basic_data)
        else:
            response = redirect(
                reverse("cata_system:seleccion_tecnica") + "?error=Técnica no valida")

        return response
    elif req.method == "POST":
        if basic_data["name_tecnica"] == "escalas" or basic_data["name_tecnica"] == "rata":
            response = PanelTagsController.controllPostEscalas(
                request=req, data=basic_data)
        else:
            response = redirect(
                reverse("cata_system:seleccion_tecnica") + "?error=Técnica no valida")
        return response
    else:
        return JsonResponse({"message": "Método no permitido"})
