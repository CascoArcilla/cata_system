from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from controllers import ConfCodesController
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
            conf_codes_controller = ConfCodesController(data=data_basic)
            response = conf_codes_controller.getOrders(req)

        elif name_technique in ["rata", "cata", "perfil flash", "sort", "napping", "perfil_ideal"]:
            conf_codes_controller = ConfCodesController(data=data_basic)
            response = conf_codes_controller.getNoOrders(
                req, name_technique)

        else:
            response = redirect(
                reverse("cata_system:seleccion_tecnica") + "?error=Técnica no valida")

        return response
    elif req.method == "POST":
        if name_technique == "escalas":
            conf_codes_controller = ConfCodesController(data=data_basic)
            response = conf_codes_controller.postOrders(req)

        elif name_technique in ["rata", "cata", "perfil_ideal"]:
            conf_codes_controller = ConfCodesController(data=data_basic)
            response = conf_codes_controller.postNoOrders(
                req, name_technique)

        elif name_technique in ["perfil flash", "sort", "napping"]:
            conf_codes_controller = ConfCodesController(
                next_url="cata_system:creando_sesion",
                data=data_basic
            )
            response = conf_codes_controller.postNoOrders(
                req, name_technique)

        else:
            response = redirect(
                reverse("cata_system:seleccion_tecnica") + "?error=Técnica no valida")

        return response
    else:
        return JsonResponse({"message": "Método no permitido"})
