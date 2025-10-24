from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from tecnicas.controllers import PanelCodesController


def configurationPanelCodes(req: HttpRequest):
    data_basic = req.session["form_basic"]
    if not data_basic:
        req.session.flush()
        return redirect(reverse("cata_system:seleccion_tecnica") +
                        "?error=datos del formulario requerido no encontrados")

    if req.method == "GET":
        if data_basic["name_tecnica"] == "escalas":
            response = PanelCodesController.controllGetConvencional(
                req, data_basic)
        else:
            response = redirect(
                reverse("cata_system:seleccion_tecnica") + "?error=Técnica no valida")
            
        return response
    elif req.method == "POST":
        if data_basic["name_tecnica"] == "escalas":
            response = PanelCodesController.controllPostConvencional(
                req, data_basic)
        else:
            response = redirect(
                reverse("cata_system:seleccion_tecnica") + "?error=Técnica no valida")
            
        return response
    else:
        return JsonResponse({"message": "Método no permitido"})
