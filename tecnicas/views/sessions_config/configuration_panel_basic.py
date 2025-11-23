from django.shortcuts import redirect
from django.http import HttpRequest, JsonResponse
from django.urls import reverse
from tecnicas.controllers import PanelBasicController
from tecnicas.utils import deleteDataSession


def configurationPanelBasic(req: HttpRequest):
    deleteDataSession(req)

    if req.method == "GET":
        name_tecnica = req.GET["name_tecnica"]

        if name_tecnica == "escalas":
            response = PanelBasicController.controllGetEscalas(request=req)
        elif name_tecnica == "rata":
            response = PanelBasicController.controllGetRATA(request=req)
        elif name_tecnica == "cata":
            response = PanelBasicController.controllGetCATA(request=req)
        elif name_tecnica == "perfil flash":
            response = PanelBasicController.controllGetPF(request=req)
        elif name_tecnica == "sort":
            response = PanelBasicController.controllGetSort(request=req)
        else:
            response = redirect(
                reverse("cata_system:seleccion_tecnica") + "?error=Técnica no valida o sin implementar")

        return response
    elif req.method == "POST":
        name_tecnica = req.GET["name_tecnica"]

        if name_tecnica == "escalas":
            response = PanelBasicController.controllPostEscalas(
                request=req, name_tecnica=name_tecnica)
        elif name_tecnica == "rata":
            response = PanelBasicController.controllPostRATA(
                request=req, name_tecnica=name_tecnica)
        elif name_tecnica == "cata":
            response = PanelBasicController.controllPostCATA(
                request=req, name_tecnica=name_tecnica)
        elif name_tecnica == "perfil flash":
            response = PanelBasicController.controllPostPF(
                request=req, name_tecnica=name_tecnica)
        elif name_tecnica == "sort":
            response = PanelBasicController.controllPostSort(
                request=req, name_tecnica=name_tecnica)
        else:
            response = redirect(
                reverse("cata_system:seleccion_tecnica") + "?error=¡Oh, vaya! Cambio de técnica repentino, vuelve a elegir otra vez")

        return response
    else:
        return JsonResponse({"message": "Método no permitido"})
