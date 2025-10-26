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

    if req.method == "GET":
        if basic_data["name_tecnica"] == "escalas" or basic_data["name_tecnica"] == "rata":
            response = PanelCreateController.controllGetEscalas(req)
        else:
            response = redirect(
                reverse("cata_system:seleccion_tecnica") + "?error=Técnica no valida")

        return response
    if req.method == "POST":
        if basic_data["name_tecnica"] == "escalas":
            response = PanelCreateController.controllPostEscalas(req)
        elif basic_data["name_tecnica"] == "rata":
            response = PanelCreateController.controllPostRATA(req)
        else:
            response = redirect(
                reverse("cata_system:seleccion_tecnica") + "?error=Técnica no valida")

        return response
    else:
        return JsonResponse({"message": "Método no permitido"})
