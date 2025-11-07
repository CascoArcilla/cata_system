from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from tecnicas.models import EstiloPalabra
from tecnicas.controllers import PanelWordsController
from tecnicas.utils import deleteDataSession


def configurationPanelWords(req: HttpRequest):
    if not req.session.get("form_basic"):
        deleteDataSession(req)
        return redirect(reverse("cata_system:seleccion_tecnica") +
                        "?error=datos requeridos no encontrados")

    basic_data = req.session["form_basic"]
    style_words = EstiloPalabra.objects.get(id=basic_data["estilo_palabras"])

    if req.method == "GET":
        if basic_data["name_tecnica"] == "escalas" or basic_data["name_tecnica"] == "rata":
            if style_words.nombre_estilo == "atributos":
                response = PanelWordsController.controllGetEscalasAtributes(req)
            elif style_words.nombre_estilo == "vocabulario":
                response = PanelWordsController.controllGetEscalasVocabulary(req)
            else:
                response = redirect(
                    reverse("cata_system:seleccion_tecnica") + "?error=Estilo de palabras no valida")
        else:
            response = redirect(
                reverse("cata_system:seleccion_tecnica") + "?error=Técnica no valida")
        return response
    elif req.method == "POST":
        if basic_data["name_tecnica"] == "escalas" or basic_data["name_tecnica"] == "rata":
            if style_words.nombre_estilo == "atributos":
                response = PanelWordsController.controllPostEscalasAtributes(req)
            elif style_words.nombre_estilo == "vocabulario":
                response = PanelWordsController.controllPostEscalasVocabulary(req)
            else:
                response = redirect(
                    reverse("cata_system:seleccion_tecnica") + "?error=Estilo de palabras no valida")
        else:
            response = redirect(
                reverse("cata_system:seleccion_tecnica") + "?error=Técnica no valida")

        return response
    else:
        return JsonResponse({"message": "Método no permitido"})
