from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from tecnicas.controllers import PanelCreateController
from tecnicas.utils import deleteDataSession


def createSession(req: HttpRequest):
    if not req.session.get("form_basic"):
        deleteDataSession(req)
        return redirect(reverse("cata_system:seleccion_tecnica") +
                        "?error=datos requeridos no encontrados")

    basic_data = req.session["form_basic"]
    name_technique = basic_data["name_tecnica"]

    if req.method == "GET":
        if name_technique == "escalas" or name_technique == "rata" or name_technique == "cata" or name_technique == "perfil flash":
            response = PanelCreateController.controllGetEscalas(req)
        else:
            response = redirect(
                reverse("cata_system:seleccion_tecnica") + "?error=Técnica no valida")

        return response
    if req.method == "POST":
        if name_technique == "escalas":
            response = PanelCreateController.controllPostEscalas(req)
        elif name_technique == "rata":
            response = PanelCreateController.controllPostRATA(req)
        elif name_technique == "cata":
            response = PanelCreateController.controllPostCATA(req)
        elif name_technique == "perfil flash":
            response = PanelCreateController.controllPostPF(req)
        else:
            response = redirect(
                reverse("cata_system:seleccion_tecnica") + "?error=Técnica no valida")

        return response
    else:
        return JsonResponse({"message": "Método no permitido"})
