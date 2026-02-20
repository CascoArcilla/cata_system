from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from controllers import PanelCodesController
from utils import deleteDataSession


def configurationPanelCodes(req: HttpRequest):
    if not req.session["form_basic"]:
        deleteDataSession(req)
        return redirect(reverse("cata_system:seleccion_tecnica") +
                        "?error=datos del formulario requerido no encontrados")

    data_basic = req.session["form_basic"]
    name_technique = data_basic["name_tecnica"]

    if req.method == "GET":
        if name_technique == "escalas":
            response = PanelCodesController.controllGetEscalas(
                req, data_basic)
        elif name_technique in ["rata", "cata", "perfil flash", "sort", "napping", "perfil_ideal"]:
            response = PanelCodesController.controllGetWithoutOrders(
                request=req, data=data_basic, name_technique=name_technique)
        else:
            response = redirect(
                reverse("cata_system:seleccion_tecnica") + "?error=Técnica no valida")

        return response
    elif req.method == "POST":
        if name_technique == "escalas":
            response = PanelCodesController.controllPostEscalas(
                req, data_basic)
        elif name_technique in ["rata", "cata", "perfil_ideal"]:
            response = PanelCodesController.controllPostNoOrdersWithWords(
                request=req, name_technique=name_technique)
        elif name_technique in ["perfil flash", "sort", "napping"]:
            response = PanelCodesController.controllPostNoOrdersNoWords(
                request=req, name_technique=name_technique)
        else:
            response = redirect(
                reverse("cata_system:seleccion_tecnica") + "?error=Técnica no valida")

        return response
    else:
        return JsonResponse({"message": "Método no permitido"})
