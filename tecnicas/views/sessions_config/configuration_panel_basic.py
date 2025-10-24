from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse
from django.urls import reverse
from tecnicas.forms import SesionBasicForm
from tecnicas.controllers import PanelBasicController


def configurationPanelBasic(req: HttpRequest):
    keys_forms = [
        "form_basic",
        "form_tags",
        "form_codes",
        "form_words"
    ]

    for key in keys_forms:
        if key in req.session:
            del req.session[key]

    if req.method == "GET":
        name_tecnica = req.GET["name_tecnica"]

        if name_tecnica == "escalas":
            response = PanelBasicController.controllGetConvencional(request=req)
        else:
            response = redirect(
                reverse("cata_system:seleccion_tecnica") + "?error=Técnica no valida o sin implementar")

        return response
    elif req.method == "POST":
        name_tecnica = req.GET["name_tecnica"]

        if name_tecnica == "escalas":
            response = PanelBasicController.controllPostConvencional(
                request=req, name_tecnica=name_tecnica)
        else:
            response = redirect(
                reverse("cata_system:seleccion_tecnica") + "?error=¡Oh, vaya! Cambio de técnica repentino, vuelve a elegir otra vez")

        return response
    else:
        return JsonResponse({"message": "Método no permitido"})
