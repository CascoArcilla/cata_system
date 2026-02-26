from django.shortcuts import redirect
from django.http import HttpRequest, JsonResponse
from django.urls import reverse
from tecnicas.controllers import PanelBasicController
from tecnicas.utils import deleteDataSession


def configurationPanelBasic(req: HttpRequest):
    name_tecnica = req.GET.get("name_tecnica")
    url_main = reverse(req.session["sensorial_url_main"]) + "?error=Técnica no valida o sin implementar"

    if req.method == "GET":
        if name_tecnica == "escalas":
            response = PanelBasicController().controllGetEscalas(request=req)

        elif name_tecnica == "rata":
            response = PanelBasicController().controllGetRATA(request=req)

        elif name_tecnica == "cata":
            response = PanelBasicController().controllGetCATA(request=req)

        elif name_tecnica == "perfil flash":
            response = PanelBasicController().controllGetPF(request=req)

        elif name_tecnica == "sort":
            response = PanelBasicController().controllGetSort(request=req)

        elif name_tecnica == "napping":
            response = PanelBasicController().controllGetNapping(request=req)

        elif name_tecnica == "perfil_ideal":
            response = PanelBasicController().controllGetIdeal(request=req)

        else:
            response = redirect(url_main)

        return response

    elif req.method == "POST":
        if name_tecnica == "escalas":
            response = PanelBasicController().controllPostEscalas(
                request=req, name_tecnica=name_tecnica)

        elif name_tecnica == "rata":
            response = PanelBasicController().controllPostRATA(
                request=req, name_tecnica=name_tecnica)

        elif name_tecnica == "cata":
            response = PanelBasicController().controllPostCATA(
                request=req, name_tecnica=name_tecnica)

        elif name_tecnica == "perfil flash":
            response = PanelBasicController().controllPostPF(
                request=req, name_tecnica=name_tecnica)

        elif name_tecnica == "sort":
            response = PanelBasicController().controllPostSort(
                request=req, name_tecnica=name_tecnica)

        elif name_tecnica == "napping":
            response = PanelBasicController().controllPostNapping(
                request=req, name_tecnica=name_tecnica)

        elif name_tecnica == "perfil_ideal":
            response = PanelBasicController().controllPostIdeal(
                request=req, name_tecnica=name_tecnica)

        else:
            response = redirect(url_main)

        return response

    else:
        return JsonResponse({"message": "Método no permitido"})
