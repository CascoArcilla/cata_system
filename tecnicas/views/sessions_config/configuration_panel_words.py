from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from tecnicas.controllers import PanelWordsController
from tecnicas.utils import deleteDataSession


def configurationPanelWords(req: HttpRequest):
    if not req.session.get("form_basic"):
        deleteDataSession(req)
        return redirect(reverse("cata_system:seleccion_tecnica") +
                        "?error=datos requeridos no encontrados")

    basic_data = req.session["form_basic"]

    if req.method == "GET":
        if basic_data["name_tecnica"] == "escalas":
            response = PanelWordsController.controllGetEscalas(req)
        else:
            response = redirect(
                reverse("cata_system:seleccion_tecnica") + "?error=Técnica no valida")

        return response
    elif req.method == "POST":
        if basic_data["name_tecnica"] == "escalas":
            response = PanelWordsController.controllPostEscalas(req)
        else:
            response = redirect(
                reverse("cata_system:seleccion_tecnica") + "?error=Técnica no valida")
            
        return response
    else:
        return JsonResponse({"message": "Método no permitido"})
