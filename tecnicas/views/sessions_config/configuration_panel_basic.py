from django.shortcuts import redirect
from django.http import HttpRequest, JsonResponse
from django.urls import reverse
from tecnicas.controllers import PanelBasicController
from utils import deleteDataSession


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
        elif name_tecnica == "napping":
            response = PanelBasicController.controllGetNapping(request=req)
        elif name_tecnica == "perfil_ideal":
            response = PanelBasicController.controllGetIdeal(request=req)
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
        elif name_tecnica == "napping":
            response = PanelBasicController.controllPostNapping(
                request=req, name_tecnica=name_tecnica)
        elif name_tecnica == "perfil_ideal":
            response = PanelBasicController.controllPostIdeal(
                request=req, name_tecnica=name_tecnica)
        else:
            response = redirect(
                reverse("cata_system:seleccion_tecnica") + "?error=Técnica no valida o sin implementar para validar")

        return response
    else:
        return JsonResponse({"message": "Método no permitido"})
