from django.shortcuts import render
from django.http import HttpRequest
from tecnicas.forms import WordForm
from tecnicas.controllers import CreateVocabularyController


def createVocabulary(req: HttpRequest):
    url_home = req.session.get("sensorial_url_main")
    view_controller = CreateVocabularyController(url_home=url_home)

    if req.method == "GET":
        response = view_controller.controllGet(req)
        return response

    elif req.method == "POST":
        response = view_controller.controllPost(req)
        return response

    else:
        context = {"error": "Método no permitido"}
        return render(req, "tecnicas/manage_vocabulary/create-vocabulary.html", context)
