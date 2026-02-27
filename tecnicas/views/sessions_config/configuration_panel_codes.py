from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from tecnicas.controllers import PanelCodesController
from tecnicas.utils import deleteDataSession


def configurationPanelCodes(req: HttpRequest):
    url_main = req.session["sensorial_url_main"]

    if not req.session["form_basic"]:
        deleteDataSession(req)
        return redirect(
            reverse(url_main) +
            "?error=datos del formulario requerido no encontrados"
        )

    data_basic = req.session["form_basic"]
    name_technique = data_basic["name_tecnica"]

    if req.method == "GET":
        if name_technique == "escalas":
            response = PanelCodesController(
                url_main=url_main,
                url_home=url_main
            ).controllGetEscalas(
                request=req,
                data=data_basic
            )

        elif name_technique in ["rata", "cata", "perfil flash", "sort", "napping", "perfil_ideal"]:
            response = PanelCodesController(
                url_main=url_main,
                url_home=url_main
            ).controllGetNoOrders(
                request=req,
                data=data_basic,
                name_technique=name_technique
            )

        else:
            response = redirect(
                reverse(url_main) +
                "?error=Técnica no valida o sin implementar"
            )

        return response

    elif req.method == "POST":
        if name_technique == "escalas":
            response = PanelCodesController(
                url_main=url_main,
                url_home=url_main
            ).controllPostEscalas(
                request=req,
                data=data_basic
            )

        elif name_technique in ["rata", "cata", "perfil_ideal"]:
            response = PanelCodesController(
                url_main=url_main,
                url_home=url_main
            ).controllPostNoOrders(
                request=req,
                name_technique=name_technique
            )

        elif name_technique in ["perfil flash", "sort", "napping"]:
            response = PanelCodesController(
                url_next="cata_system:creando_sesion",
                url_main=url_main,
                url_home=url_main
            ).controllPostNoOrders(
                request=req,
                name_technique=name_technique
            )

        else:
            response = redirect(reverse(url_main) +
                                "?error=Técnica no valida o sin implementar")

        return response

    else:
        return JsonResponse({"message": "Método no permitido"})
