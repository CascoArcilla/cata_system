from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from tecnicas.controllers import PanelCodesController
from tecnicas.utils import deleteDataSession


def configurationPanelCodes(req: HttpRequest):
    if not req.session["form_basic"]:
        deleteDataSession(req)
        return redirect(reverse("cata_system:seleccion_tecnica") +
                        "?error=datos del formulario requerido no encontrados")
    
    data_basic = req.session["form_basic"]

    if req.method == "GET":
        if data_basic["name_tecnica"] == "escalas":
            response = PanelCodesController.controllGetEscalas(
                req, data_basic)
        else:
            response = redirect(
                reverse("cata_system:seleccion_tecnica") + "?error=Técnica no valida")
            
        return response
    elif req.method == "POST":
        if data_basic["name_tecnica"] == "escalas":
            response = PanelCodesController.controllPostEscalas(
                req, data_basic)
        else:
            response = redirect(
                reverse("cata_system:seleccion_tecnica") + "?error=Técnica no valida")
            
        return response
    else:
        return JsonResponse({"message": "Método no permitido"})
