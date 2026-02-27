from django.shortcuts import render
from django.http import HttpRequest
from tecnicas.controllers import ViewVocabularyController
from tecnicas.utils import general_error


def viewVocabulary(req: HttpRequest, nombre_vocabulario: str):
    url_home = req.session.get("sensorial_url_main")
    view_controller = ViewVocabularyController(url_home=url_home)

    if req.method == "GET":
        response = view_controller.controllGet(req, nombre_vocabulario)
        return response
    else:
        return general_error("Método no permitido")
