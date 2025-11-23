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
    name_technique = data_basic["name_tecnica"]

    if req.method == "GET":
        if name_technique == "escalas":
            response = PanelCodesController.controllGetEscalas(
                req, data_basic)
        elif name_technique == "rata" or name_technique == "cata" or name_technique == "perfil flash" or name_technique == "sort":
            response = PanelCodesController.controllGetRATA(
                request=req, data=data_basic, name_technique=name_technique)
        else:
            response = redirect(
                reverse("cata_system:seleccion_tecnica") + "?error=Técnica no valida")

        return response
    elif req.method == "POST":
        if name_technique == "escalas":
            response = PanelCodesController.controllPostEscalas(
                req, data_basic)
        elif name_technique == "rata":
            response = PanelCodesController.controllPostRATA(request=req)
        elif name_technique == "cata":
            response = PanelCodesController.controllPostRATA(
                request=req, is_rata=False)
        elif name_technique == "perfil flash":
            response = PanelCodesController.controllPostPF(
                request=req)
        elif name_technique == "sort":
            response = PanelCodesController.controllPostSort(
                request=req)
        else:
            response = redirect(
                reverse("cata_system:seleccion_tecnica") + "?error=Técnica no valida")

        return response
    else:
        return JsonResponse({"message": "Método no permitido"})
