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
    name_technique = basic_data["name_tecnica"]

    if req.method == "GET":
        if name_technique == "escalas" or name_technique == "rata" or name_technique == "perfil flash":
            response = PanelTagsController.controllGetEscalas(
                request=req, data=basic_data)
        else:
            response = redirect(
                reverse("cata_system:seleccion_tecnica") + "?error=Técnica no valida")

        return response
    elif req.method == "POST":
        if name_technique == "escalas" or name_technique == "rata" or name_technique == "perfil flash":
            response = PanelTagsController.controllPostEscalas(
                request=req, data=basic_data)
        else:
            response = redirect(
                reverse("cata_system:seleccion_tecnica") + "?error=Técnica no valida")
        return response
    else:
        return JsonResponse({"message": "Método no permitido"})
