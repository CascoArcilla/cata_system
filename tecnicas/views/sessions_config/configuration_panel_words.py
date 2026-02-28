from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from controllers import PanelWordsController
from utils import deleteDataSession


def configurationPanelWords(req: HttpRequest):
    url_main = req.session["sensorial_url_main"]

    if not req.session.get("form_basic"):
        deleteDataSession(req)
        return redirect(reverse(url_main) +
                        "?error=datos requeridos no encontrados")

    basic_data = req.session["form_basic"]
    name_technique = basic_data["name_tecnica"]
    style_words = basic_data["estilo_palabras"]

    if req.method == "GET":
        if name_technique in ["escalas", "rata", "cata", "perfil_ideal"]:
            if style_words == "atributos":
                response = PanelWordsController(
                    url_main=url_main,
                    url_home=url_main
                ).controllGetAtributes(req)

            elif style_words == "vocabulario":
                response = PanelWordsController(
                    url_main=url_main,
                    url_home=url_main
                ).controllGetVocabulary(req)

            else:
                response = redirect(reverse(url_main) +
                                    "?error=Estilo de palabras no valida")

        else:
            response = redirect(reverse(url_main) +
                                "?error=Técnica no valida o sin implementar")

        return response

    elif req.method == "POST":
        if name_technique in ["escalas", "rata", "cata", "perfil_ideal"]:
            if style_words == "atributos":
                response = PanelWordsController(
                    url_main=url_main,
                    url_home=url_main
                ).controllPostAtributes(req)

            elif style_words == "vocabulario":
                response = PanelWordsController(
                    url_main=url_main,
                    url_home=url_main
                ).controllPostVocabulary(req)

            else:
                response = redirect(
                    reverse(url_main) +
                    "?error=Estilo de palabras no valida"
                )

        else:
            response = redirect(
                reverse(url_main) +
                "?error=Técnica no valida o sin implementar"
            )

        return response

    else:
        return JsonResponse({"message": "Método no permitido"})
