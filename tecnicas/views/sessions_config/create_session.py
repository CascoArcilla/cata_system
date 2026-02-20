from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from controllers import PanelCreateEscalasController, PanelCreateRataController, PanelCreateCataController, PanelCreatePFController, PanelCreateSortController, PanelCreateNappingController, PanelCreateIdealController
from utils import deleteDataSession


def createSession(req: HttpRequest):
    if not req.session.get("form_basic"):
        deleteDataSession(req)
        return redirect(reverse("cata_system:seleccion_tecnica") +
                        "?error=datos requeridos no encontrados")

    basic_data = req.session["form_basic"]
    name_technique = basic_data["name_tecnica"]

    if req.method == "GET":
        if name_technique == "escalas":
            response = PanelCreateEscalasController.controllGet(req)
        elif name_technique == "rata":
            response = PanelCreateRataController.controllGet(req)
        elif name_technique == "cata":
            response = PanelCreateCataController.controllGet(req)
        elif name_technique == "perfil flash":
            response = PanelCreatePFController.controllGet(req)
        elif name_technique == "sort":
            response = PanelCreateSortController.controllGet(req)
        elif name_technique == "napping":
            response = PanelCreateNappingController.controllGet(req)
        elif name_technique == "perfil_ideal":
            response = PanelCreateIdealController.controllGet(req)
        else:
            response = redirect(
                reverse("cata_system:seleccion_tecnica") + "?error=Técnica no valida")

        return response
    if req.method == "POST":
        if name_technique == "escalas":
            response = PanelCreateEscalasController.controllPost(req)
        elif name_technique == "rata":
            response = PanelCreateRataController.controllPost(req)
        elif name_technique == "cata":
            response = PanelCreateCataController.controllPost(req)
        elif name_technique == "perfil flash":
            response = PanelCreatePFController.controllPost(req)
        elif name_technique == "sort":
            response = PanelCreateSortController.controllPost(req)
        elif name_technique == "napping":
            response = PanelCreateNappingController.controllPost(req)
        elif name_technique == "perfil_ideal":
            response = PanelCreateIdealController.controllPost(req)
        else:
            response = redirect(
                reverse("cata_system:seleccion_tecnica") + "?error=Técnica no valida")

        return response
    else:
        return JsonResponse({"message": "Método no permitido"})
