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
    name_technique = basic_data["name_tecnica"]
    style_words = basic_data["estilo_palabras"]

    if req.method == "GET":
        if name_technique in ["escalas", "rata", "cata", "perfil_ideal"]:
            if style_words == "atributos":
                response = PanelWordsController.controllGetAtributes(
                    req)
            elif style_words == "vocabulario":
                response = PanelWordsController.controllGetVocabulary(
                    req)
            else:
                response = redirect(
                    reverse("cata_system:seleccion_tecnica") + "?error=Estilo de palabras no valida")
        else:
            response = redirect(
                reverse("cata_system:seleccion_tecnica") + "?error=Técnica no valida")
        return response

    elif req.method == "POST":
        if name_technique in ["escalas", "rata", "cata", "perfil_ideal"]:
            if style_words == "atributos":
                response = PanelWordsController.controllPostAtributes(
                    req)
            elif style_words == "vocabulario":
                response = PanelWordsController.controllPostVocabulary(
                    req)
            else:
                response = redirect(
                    reverse("cata_system:seleccion_tecnica") + "?error=Estilo de palabras no valida")
        else:
            response = redirect(
                reverse("cata_system:seleccion_tecnica") + "?error=Técnica no valida")

        return response

    else:
        return JsonResponse({"message": "Método no permitido"})
