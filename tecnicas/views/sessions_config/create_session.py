from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from controllers import PanelCreateEscalasController, PanelCreateRataController, PanelCreateCataController, PanelCreatePFController, PanelCreateSortController, PanelCreateNappingController, PanelCreateIdealController
from utils import deleteDataSession, delete_images


def createSession(req: HttpRequest):
    url_main = req.session.get("sensorial_url_main")

    if not req.session.get("form_basic"):
        images_cata = req.session.get("form_images_cata", {})
        if images_cata:
            delete_images(list(images_cata.values()))
        deleteDataSession(req)
        return redirect(reverse(url_main) + "?error=datos requeridos no encontrados")

    basic_data = req.session["form_basic"]
    name_technique = basic_data["name_tecnica"]

    if req.method == "GET":
        if name_technique == "escalas":
            response = PanelCreateEscalasController(url_home=url_main).controllGet(req)
        elif name_technique == "rata":
            response = PanelCreateRataController(url_home=url_main).controllGet(req)
        elif name_technique == "cata":
            response = PanelCreateCataController(url_home=url_main).controllGet(req)
        elif name_technique == "perfil flash":
            response = PanelCreatePFController(url_home=url_main).controllGet(req)
        elif name_technique == "sort":
            response = PanelCreateSortController(url_home=url_main).controllGet(req)
        elif name_technique == "napping":
            response = PanelCreateNappingController(url_home=url_main).controllGet(req)
        elif name_technique == "perfil_ideal":
            response = PanelCreateIdealController(url_home=url_main).controllGet(req)
        else:
            response = redirect(
                reverse(url_main) + "?error=Técnica no valida")

        return response
    if req.method == "POST":
        if name_technique == "escalas":
            response = PanelCreateEscalasController(url_home=url_main).controllPost(req)
        elif name_technique == "rata":
            response = PanelCreateRataController(url_home=url_main).controllPost(req)
        elif name_technique == "cata":
            response = PanelCreateCataController(url_home=url_main).controllPost(req)
        elif name_technique == "perfil flash":
            response = PanelCreatePFController(url_home=url_main).controllPost(req)
        elif name_technique == "sort":
            response = PanelCreateSortController(url_home=url_main).controllPost(req)
        elif name_technique == "napping":
            response = PanelCreateNappingController(url_home=url_main).controllPost(req)
        elif name_technique == "perfil_ideal":
            response = PanelCreateIdealController(url_home=url_main).controllPost(req)
        else:
            response = redirect(
                reverse(url_main) + "?error=Técnica no valida")

        return response
    else:
        return JsonResponse({"message": "Método no permitido"})
