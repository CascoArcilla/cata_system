from django.shortcuts import redirect
from django.http import HttpRequest, JsonResponse
from django.urls import reverse
from controllers import PanelBasicController


def configurationPanelBasic(req: HttpRequest):
    name_tecnica = req.GET.get("name_tecnica")
    url_main = req.session["sensorial_url_main"]

    if req.method == "GET":
        if name_tecnica == "escalas":
            response = PanelBasicController(
                url_main=url_main,
                url_home=url_main
            ).controllGetEscalas(request=req)

        elif name_tecnica == "rata":
            response = PanelBasicController(
                url_main=url_main,
                url_home=url_main,
                template="create_sesion/conf-panel-basic-rata.html"
            ).controllGetRATA(request=req)

        elif name_tecnica == "cata":
            response = PanelBasicController(
                url_main=url_main,
                url_home=url_main,
                template="create_sesion/conf-panel-basic-cata.html"
            ).controllGetCATA(request=req)

        elif name_tecnica == "perfil flash":
            response = PanelBasicController(
                url_main=url_main,
                url_home=url_main,
                template="create_sesion/conf-panel-basic-pf.html"
            ).controllGetPF(request=req)

        elif name_tecnica == "sort":
            response = PanelBasicController(
                url_main=url_main,
                url_home=url_main,
                template="create_sesion/conf-panel-basic-sort.html"
            ).controllGetSort(request=req)

        elif name_tecnica == "napping":
            response = PanelBasicController(
                url_main=url_main,
                url_home=url_main,
                template="create_sesion/conf-panel-basic-napping.html"
            ).controllGetNapping(request=req)

        elif name_tecnica == "perfil_ideal":
            response = PanelBasicController(
                url_main=url_main,
                url_home=url_main,
                template="create_sesion/conf-panel-basic-ideal.html"
            ).controllGetIdeal(request=req)

        else:
            response = redirect(reverse(url_main) + "?error=Técnica no valida o sin implementar")

        return response

    elif req.method == "POST":
        if name_tecnica == "escalas":
            response = PanelBasicController(
                url_home=url_main,
                url_main=url_main
            ).controllPostEscalas(
                request=req, name_tecnica=name_tecnica)

        elif name_tecnica == "rata":
            response = PanelBasicController(
                url_home=url_main,
                url_main=url_main,
                template="create_sesion/conf-panel-basic-rata.html"
            ).controllPostRATA(
                request=req, name_tecnica=name_tecnica)

        elif name_tecnica == "cata":
            response = PanelBasicController(
                url_home=url_main,
                url_main=url_main,
                template="create_sesion/conf-panel-basic-cata.html"
            ).controllPostCATA(
                request=req, name_tecnica=name_tecnica)

        elif name_tecnica == "perfil flash":
            response = PanelBasicController(
                url_home=url_main,
                url_main=url_main,
                template="create_sesion/conf-panel-basic-pf.html"
            ).controllPostPF(
                request=req, name_tecnica=name_tecnica)

        elif name_tecnica == "sort":
            response = PanelBasicController(
                url_home=url_main,
                url_main=url_main,
                template="create_sesion/conf-panel-basic-sort.html"
            ).controllPostSort(
                request=req, name_tecnica=name_tecnica)

        elif name_tecnica == "napping":
            response = PanelBasicController(
                url_home=url_main,
                url_main=url_main,
                template="create_sesion/conf-panel-basic-napping.html"
            ).controllPostNapping(
                request=req, name_tecnica=name_tecnica)

        elif name_tecnica == "perfil_ideal":
            response = PanelBasicController(
                url_home=url_main,
                url_main=url_main,
                template="create_sesion/conf-panel-basic-ideal.html"
            ).controllPostIdeal(
                request=req, name_tecnica=name_tecnica)

        else:
            response = redirect(reverse(url_main) + "?error=Técnica no valida o sin implementar")

        return response

    else:
        return JsonResponse({"message": "Método no permitido"})
